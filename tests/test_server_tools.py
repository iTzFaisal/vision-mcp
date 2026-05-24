class TestToolRegistration:
    def test_tool_names_have_vision_prefix(self, mcp_instance):
        tools = mcp_instance._tool_manager._tools
        assert "vision_analyze_image" in tools
        assert "vision_compare_images" in tools

    def test_analyze_image_has_name(self, mcp_instance):
        tool = mcp_instance._tool_manager._tools["vision_analyze_image"]
        assert tool.name == "vision_analyze_image"

    def test_compare_images_has_name(self, mcp_instance):
        tool = mcp_instance._tool_manager._tools["vision_compare_images"]
        assert tool.name == "vision_compare_images"


class TestToolAnnotations:
    def test_analyze_image_annotations(self, mcp_instance):
        tool = mcp_instance._tool_manager._tools["vision_analyze_image"]
        annotations = tool.annotations
        assert annotations is not None
        assert annotations.readOnlyHint is True
        assert annotations.destructiveHint is False
        assert annotations.idempotentHint is True
        assert annotations.openWorldHint is True
        assert annotations.title == "Vision Analyze Image"

    def test_compare_images_annotations(self, mcp_instance):
        tool = mcp_instance._tool_manager._tools["vision_compare_images"]
        annotations = tool.annotations
        assert annotations is not None
        assert annotations.readOnlyHint is True
        assert annotations.destructiveHint is False
        assert annotations.idempotentHint is True
        assert annotations.openWorldHint is True
        assert annotations.title == "Vision Compare Images"


class TestToolDocstrings:
    def test_analyze_image_description(self, mcp_instance):
        tool = mcp_instance._tool_manager._tools["vision_analyze_image"]
        description = tool.description
        assert "Analyze a single image" in description
        assert "Supports PNG, JPEG, GIF, and WebP" in description
        assert "20MB" in description
        assert "Args:" in description
        assert "Returns:" in description
        assert "Error Handling:" in description

    def test_compare_images_description(self, mcp_instance):
        tool = mcp_instance._tool_manager._tools["vision_compare_images"]
        description = tool.description
        assert "Compare multiple images" in description
        assert "Supports PNG" in description
        assert "GIF" in description
        assert "WebP" in description
        assert "20MB" in description
        assert "Args:" in description
        assert "Returns:" in description
        assert "Error Handling:" in description


class TestToolMetadata:
    def test_both_tools_are_async(self, mcp_instance):
        for tool in mcp_instance._tool_manager._tools.values():
            assert tool.is_async is True

    def test_tools_have_parameters(self, mcp_instance):
        for tool in mcp_instance._tool_manager._tools.values():
            assert tool.parameters is not None
