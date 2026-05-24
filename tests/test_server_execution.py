import pytest
from vision_mcp.models import AnalyzeImageInput, CompareImagesInput
from vision_mcp.server import analyze_image, compare_images


@pytest.mark.asyncio
class TestAnalyzeImageExecution:
    async def test_success(self, mock_encode_image, mock_call_vision_api):
        params = AnalyzeImageInput(
            image_path="/path/to/image.png",
            prompt="Describe this",
        )
        result = await analyze_image(params)
        assert result == "Mock vision API response"
        mock_encode_image.assert_called_once_with("/path/to/image.png")
        mock_call_vision_api.assert_called_once()

    async def test_file_not_found(self, mock_encode_image_error, mock_call_vision_api):
        params = AnalyzeImageInput(
            image_path="/nonexistent.png",
            prompt="Describe this",
        )
        result = await analyze_image(params)
        assert "Mock file not found" in result
        mock_encode_image_error.assert_called_once()
        mock_call_vision_api.assert_not_called()

    async def test_api_error(self, mock_encode_image, mock_call_vision_api_error):
        params = AnalyzeImageInput(
            image_path="/path/to/image.png",
            prompt="Describe this",
        )
        result = await analyze_image(params)
        assert result == "Error: Mock API error"
        mock_encode_image.assert_called_once()
        mock_call_vision_api_error.assert_called_once()

    async def test_uses_params_prompt(self, mock_encode_image, mock_call_vision_api):
        params = AnalyzeImageInput(
            image_path="/path/to/image.png",
            prompt="Custom prompt",
        )
        result = await analyze_image(params)
        assert result == "Mock vision API response"
        call_args = mock_call_vision_api.call_args[0]
        content_blocks = call_args[0]
        assert content_blocks[1] == {"type": "text", "text": "Custom prompt"}

    async def test_default_prompt(self, mock_encode_image, mock_call_vision_api):
        params = AnalyzeImageInput(image_path="/path/to/image.png")
        result = await analyze_image(params)
        assert result == "Mock vision API response"
        call_args = mock_call_vision_api.call_args[0]
        content_blocks = call_args[0]
        assert content_blocks[1]["text"] == "Describe this image in detail."

    async def test_includes_image_content_block(self, mock_encode_image, mock_call_vision_api):
        params = AnalyzeImageInput(
            image_path="/path/to/image.png",
            prompt="Describe this",
        )
        await analyze_image(params)
        call_args = mock_call_vision_api.call_args[0]
        content_blocks = call_args[0]
        assert content_blocks[0]["type"] == "image_url"
        assert "data:image/png;base64," in content_blocks[0]["image_url"]["url"]
        assert content_blocks[0]["image_url"]["detail"] == "high"


@pytest.mark.asyncio
class TestCompareImagesExecution:
    async def test_success(self, mock_encode_image, mock_call_vision_api):
        params = CompareImagesInput(
            image_paths=["/path/a.png", "/path/b.png"],
            prompt="Compare these",
        )
        result = await compare_images(params)
        assert result == "Mock vision API response"
        assert mock_encode_image.call_count == 2
        mock_call_vision_api.assert_called_once()

    async def test_file_not_found(self, mock_encode_image_error, mock_call_vision_api):
        params = CompareImagesInput(
            image_paths=["/path/a.png", "/path/b.png"],
            prompt="Compare these",
        )
        result = await compare_images(params)
        assert "Mock file not found" in result
        mock_encode_image_error.assert_called_once()
        mock_call_vision_api.assert_not_called()

    async def test_api_error(self, mock_encode_image, mock_call_vision_api_error):
        params = CompareImagesInput(
            image_paths=["/path/a.png", "/path/b.png"],
            prompt="Compare these",
        )
        result = await compare_images(params)
        assert result == "Error: Mock API error"
        mock_call_vision_api_error.assert_called_once()

    async def test_multiple_images_encoded(self, mock_encode_image, mock_call_vision_api):
        paths = ["/path/a.png", "/path/b.png", "/path/c.png"]
        params = CompareImagesInput(image_paths=paths, prompt="Compare")
        await compare_images(params)
        assert mock_encode_image.call_count == 3
        assert mock_encode_image.call_args_list[0][0] == ("/path/a.png",)
        assert mock_encode_image.call_args_list[1][0] == ("/path/b.png",)
        assert mock_encode_image.call_args_list[2][0] == ("/path/c.png",)

    async def test_includes_image_labels(self, mock_encode_image, mock_call_vision_api):
        params = CompareImagesInput(
            image_paths=["/path/a.png", "/path/b.png"],
            prompt="Compare",
        )
        await compare_images(params)
        call_args = mock_call_vision_api.call_args[0]
        content_blocks = call_args[0]
        texts = [b["text"] for b in content_blocks if b["type"] == "text"]
        assert "Image 1:" in texts
        assert "Image 2:" in texts
        assert "Compare" in texts

    async def test_content_block_structure(self, mock_encode_image, mock_call_vision_api):
        params = CompareImagesInput(
            image_paths=["/path/a.png", "/path/b.png"],
            prompt="Compare",
        )
        await compare_images(params)
        call_args = mock_call_vision_api.call_args[0]
        content_blocks = call_args[0]
        assert content_blocks[0]["type"] == "image_url"
        assert content_blocks[0]["image_url"]["detail"] == "high"
        assert content_blocks[1]["type"] == "text"
        assert content_blocks[1]["text"] == "Image 1:"
