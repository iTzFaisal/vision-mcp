from mcp.server.fastmcp import FastMCP
from .image_utils import encode_image
from .client import call_vision_api, VisionAPIError
from .models import AnalyzeImageInput, CompareImagesInput

mcp = FastMCP("vision_mcp")


@mcp.tool(
    name="vision_analyze_image",
    annotations={
        "title": "Vision Analyze Image",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def analyze_image(params: AnalyzeImageInput) -> str:
    """Analyze a single image using a vision-capable model.

    Sends the image to the configured vision model along with a text prompt
    and returns the model's response. Supports PNG, JPEG, GIF, and WebP
    formats up to 20MB.

    Args:
        params: An AnalyzeImageInput model containing:
            image_path: Path to the image file to analyze.
            prompt: Text prompt describing what to analyze (defaults to
                "Describe this image in detail.").

    Returns:
        The vision model's text response as a string.

    Error Handling:
        - FileNotFoundError: if the image file does not exist.
        - PermissionError: if the image file is not readable.
        - ValueError: if the image format is unsupported or the file is too large.
        - VisionAPIError: if the API request fails or returns an error.
    """
    content_blocks = []

    try:
        data_uri = encode_image(params.image_path)
    except (FileNotFoundError, PermissionError, ValueError) as e:
        return str(e)

    content_blocks.append(
        {"type": "image_url", "image_url": {"url": data_uri, "detail": "high"}}
    )
    content_blocks.append({"type": "text", "text": params.prompt})

    try:
        return await call_vision_api(content_blocks)
    except VisionAPIError as e:
        return f"Error: {e}"


@mcp.tool(
    name="vision_compare_images",
    annotations={
        "title": "Vision Compare Images",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def compare_images(params: CompareImagesInput) -> str:
    """Compare multiple images using a vision-capable model.

    Sends two to eight images to the configured vision model along with a
    comparison prompt and returns the model's response. Supports PNG, JPEG,
    GIF, and WebP formats up to 20MB each.

    Args:
        params: A CompareImagesInput model containing:
            image_paths: List of paths to image files to compare (2–8).
            prompt: Text prompt describing what to compare across the images.

    Returns:
        The vision model's text response as a string.

    Error Handling:
        - FileNotFoundError: if any image file does not exist.
        - PermissionError: if any image file is not readable.
        - ValueError: if any image format is unsupported or a file is too large.
        - VisionAPIError: if the API request fails or returns an error.
    """
    content_blocks = []

    for i, path in enumerate(params.image_paths, start=1):
        try:
            data_uri = encode_image(path)
        except (FileNotFoundError, PermissionError, ValueError) as e:
            return f"Error with image {i} ({path}): {e}"

        content_blocks.append(
            {"type": "image_url", "image_url": {"url": data_uri, "detail": "high"}}
        )
        content_blocks.append({"type": "text", "text": f"Image {i}:"})

    content_blocks.append({"type": "text", "text": params.prompt})

    try:
        return await call_vision_api(content_blocks)
    except VisionAPIError as e:
        return f"Error: {e}"


def main():
    mcp.run()
