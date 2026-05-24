import pytest
from pydantic import ValidationError
from vision_mcp.models import AnalyzeImageInput, CompareImagesInput, DEFAULT_ANALYZE_PROMPT


class TestAnalyzeImageInput:
    def test_valid_input(self):
        model = AnalyzeImageInput(
            image_path="/path/to/image.png",
            prompt="Describe this",
        )
        assert model.image_path == "/path/to/image.png"
        assert model.prompt == "Describe this"

    def test_default_prompt(self):
        model = AnalyzeImageInput(image_path="/path/to/image.png")
        assert model.prompt == DEFAULT_ANALYZE_PROMPT

    def test_empty_image_path(self):
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeImageInput(image_path="", prompt="Describe this")
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("image_path",) for e in errors)

    def test_empty_prompt(self):
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeImageInput(image_path="/path/to/image.png", prompt="")
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("prompt",) for e in errors)

    def test_extra_field(self):
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeImageInput(
                image_path="/path/to/image.png",
                prompt="Describe this",
                extra_field="unexpected",
            )
        errors = exc_info.value.errors()
        assert any("Extra inputs are not permitted" in e["msg"] for e in errors)

    def test_missing_image_path(self):
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeImageInput(prompt="Describe this")
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("image_path",) for e in errors)

    def test_strips_whitespace(self):
        model = AnalyzeImageInput(
            image_path="  /path/to/image.png  ",
            prompt="  Describe this  ",
        )
        assert model.image_path == "/path/to/image.png"
        assert model.prompt == "Describe this"

    def test_prompt_max_length(self):
        long_prompt = "x" * 4001
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeImageInput(
                image_path="/path/to/image.png",
                prompt=long_prompt,
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("prompt",) for e in errors)


class TestCompareImagesInput:
    def test_valid_input(self):
        model = CompareImagesInput(
            image_paths=["/path/a.png", "/path/b.png"],
            prompt="Compare these",
        )
        assert model.image_paths == ["/path/a.png", "/path/b.png"]
        assert model.prompt == "Compare these"

    def test_too_few_images(self):
        with pytest.raises(ValidationError) as exc_info:
            CompareImagesInput(
                image_paths=["/path/a.png"],
                prompt="Compare these",
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("image_paths",) for e in errors)

    def test_too_many_images(self):
        with pytest.raises(ValidationError) as exc_info:
            CompareImagesInput(
                image_paths=[f"/path/{i}.png" for i in range(9)],
                prompt="Compare these",
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("image_paths",) for e in errors)

    def test_empty_prompt(self):
        with pytest.raises(ValidationError) as exc_info:
            CompareImagesInput(
                image_paths=["/path/a.png", "/path/b.png"],
                prompt="",
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("prompt",) for e in errors)

    def test_missing_image_paths(self):
        with pytest.raises(ValidationError) as exc_info:
            CompareImagesInput(prompt="Compare these")
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("image_paths",) for e in errors)

    def test_missing_prompt(self):
        with pytest.raises(ValidationError) as exc_info:
            CompareImagesInput(image_paths=["/path/a.png", "/path/b.png"])
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("prompt",) for e in errors)

    def test_extra_field(self):
        with pytest.raises(ValidationError) as exc_info:
            CompareImagesInput(
                image_paths=["/path/a.png", "/path/b.png"],
                prompt="Compare these",
                extra="nope",
            )
        errors = exc_info.value.errors()
        assert any("Extra inputs are not permitted" in e["msg"] for e in errors)

    def test_strips_whitespace(self):
        model = CompareImagesInput(
            image_paths=["  /path/a.png  ", "  /path/b.png  "],
            prompt="  Compare these  ",
        )
        assert model.image_paths == ["/path/a.png", "/path/b.png"]
        assert model.prompt == "Compare these"

    def test_prompt_max_length(self):
        long_prompt = "x" * 4001
        with pytest.raises(ValidationError) as exc_info:
            CompareImagesInput(
                image_paths=["/path/a.png", "/path/b.png"],
                prompt=long_prompt,
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("prompt",) for e in errors)
