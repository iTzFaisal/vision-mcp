from pydantic import BaseModel, ConfigDict, Field

DEFAULT_ANALYZE_PROMPT = "Describe this image in detail."


class AnalyzeImageInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    image_path: str = Field(
        ...,
        min_length=1,
        description="Path to the image file to analyze. Supports PNG, JPEG, GIF, and WebP formats up to 20MB.",
        examples=["/path/to/image.png"],
    )
    prompt: str = Field(
        default=DEFAULT_ANALYZE_PROMPT,
        min_length=1,
        max_length=4000,
        description="Text prompt describing what to analyze about the image.",
        examples=["Describe this image in detail."],
    )


class CompareImagesInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    image_paths: list[str] = Field(
        ...,
        min_length=2,
        max_length=8,
        description="List of paths to image files to compare. Minimum 2, maximum 8. Supports PNG, JPEG, GIF, and WebP formats up to 20MB each.",
        examples=[["/path/to/image1.png", "/path/to/image2.png"]],
    )
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Text prompt describing what to compare across the images.",
        examples=["Compare the differences between these two images."],
    )
