class TestToolRegistration:
    def test_tool_names_have_vision_prefix(self, tools):
        names = [t.name for t in tools]
        assert "vision_analyze_image" in names
        assert "vision_compare_images" in names

    def test_analyze_image_has_name(self, analyze_tool):
        assert analyze_tool.name == "vision_analyze_image"

    def test_compare_images_has_name(self, compare_tool):
        assert compare_tool.name == "vision_compare_images"


class TestToolAnnotations:
    def test_analyze_image_annotations(self, analyze_tool):
        annotations = analyze_tool.annotations
        assert annotations is not None
        assert annotations.read_only_hint is True
        assert annotations.destructive_hint is False
        assert annotations.idempotent_hint is True
        assert annotations.open_world_hint is True
        assert annotations.title == "Vision Analyze Image"

    def test_compare_images_annotations(self, compare_tool):
        annotations = compare_tool.annotations
        assert annotations is not None
        assert annotations.read_only_hint is True
        assert annotations.destructive_hint is False
        assert annotations.idempotent_hint is True
        assert annotations.open_world_hint is True
        assert annotations.title == "Vision Compare Images"


class TestToolDocstrings:
    def test_analyze_image_description(self, analyze_tool):
        description = analyze_tool.description
        assert "Analyze a single image" in description
        assert "Supports PNG, JPEG, GIF, and WebP" in description
        assert "20MB" in description

    def test_compare_images_description(self, compare_tool):
        description = compare_tool.description
        assert "Compare multiple images" in description
        assert "Supports PNG" in description
        assert "GIF" in description
        assert "WebP" in description
        assert "20MB" in description


class TestToolInputSchema:
    def test_analyze_image_has_image_path_param(self, analyze_tool):
        props = analyze_tool.input_schema.get("properties", {})
        assert "image_path" in props

    def test_analyze_image_has_prompt_param(self, analyze_tool):
        props = analyze_tool.input_schema.get("properties", {})
        assert "prompt" in props

    def test_compare_images_has_image_paths_param(self, compare_tool):
        props = compare_tool.input_schema.get("properties", {})
        assert "image_paths" in props

    def test_compare_images_has_prompt_param(self, compare_tool):
        props = compare_tool.input_schema.get("properties", {})
        assert "prompt" in props

    def test_image_path_has_min_length(self, analyze_tool):
        prop = analyze_tool.input_schema["properties"]["image_path"]
        assert prop.get("minLength") == 1

    def test_prompt_has_max_length(self, analyze_tool):
        prop = analyze_tool.input_schema["properties"]["prompt"]
        assert prop.get("maxLength") == 4000

    def test_prompt_has_default(self, analyze_tool):
        prop = analyze_tool.input_schema["properties"]["prompt"]
        assert prop.get("default") == "Describe this image in detail."

    def test_image_paths_has_min_items(self, compare_tool):
        prop = compare_tool.input_schema["properties"]["image_paths"]
        assert prop.get("minItems") == 2

    def test_image_paths_has_max_items(self, compare_tool):
        prop = compare_tool.input_schema["properties"]["image_paths"]
        assert prop.get("maxItems") == 8
