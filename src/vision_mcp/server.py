from mcp.server import FastMCP
from .image_utils import encode_image
from .client import call_vision_api, VisionAPIError

mcp = FastMCP("vision-mcp")

DEFAULT_ANALYZE_PROMPT = "Describe this image in detail."


@mcp.tool()
async def analyze_image(image_path: str, prompt: str = DEFAULT_ANALYZE_PROMPT) -> str:
    content_blocks = []

    try:
        data_uri = encode_image(image_path)
    except (FileNotFoundError, PermissionError, ValueError) as e:
        return str(e)

    content_blocks.append(
        {"type": "image_url", "image_url": {"url": data_uri, "detail": "high"}}
    )
    content_blocks.append({"type": "text", "text": prompt})

    try:
        return await call_vision_api(content_blocks)
    except VisionAPIError as e:
        return f"Error: {e}"


@mcp.tool()
async def compare_images(image_paths: list[str], prompt: str) -> str:
    if not prompt:
        return "Error: A prompt is required for image comparison"

    if len(image_paths) < 2:
        return (
            "Error: At least 2 images are required for comparison. "
            "Use analyze_image for single-image analysis."
        )

    if len(image_paths) > 8:
        return "Error: Maximum 8 images allowed for comparison"

    content_blocks = []

    for i, path in enumerate(image_paths, start=1):
        try:
            data_uri = encode_image(path)
        except (FileNotFoundError, PermissionError, ValueError) as e:
            return f"Error with image {i} ({path}): {e}"

        content_blocks.append(
            {"type": "image_url", "image_url": {"url": data_uri, "detail": "high"}}
        )
        content_blocks.append({"type": "text", "text": f"Image {i}:"})

    content_blocks.append({"type": "text", "text": prompt})

    try:
        return await call_vision_api(content_blocks)
    except VisionAPIError as e:
        return f"Error: {e}"


def main():
    mcp.run()
