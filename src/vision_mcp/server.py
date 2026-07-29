import asyncio

from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    ListToolsResult,
    TextContent,
    Tool,
    ToolAnnotations,
)

from .client import call_vision_api
from .image_utils import encode_image
from .models import AnalyzeImageInput, CompareImagesInput

ANALYZE_TOOL = Tool(
    name="vision_analyze_image",
    title="Vision Analyze Image",
    description="""Analyze a single image using a vision-capable model.

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
    - VisionAPIError: if the API request fails or returns an error.""",
    input_schema=AnalyzeImageInput.model_json_schema(),
    annotations=ToolAnnotations(
        title="Vision Analyze Image",
        read_only_hint=True,
        destructive_hint=False,
        idempotent_hint=True,
        open_world_hint=True,
    ),
)

COMPARE_TOOL = Tool(
    name="vision_compare_images",
    title="Vision Compare Images",
    description="""Compare multiple images using a vision-capable model.

Sends two to eight images to the configured vision model along with a
comparison prompt and returns the model's response. Supports PNG, JPEG,
GIF, and WebP formats up to 20MB each.

Args:
    params: A CompareImagesInput model containing:
        image_paths: List of paths to image files to compare (2-8).
        prompt: Text prompt describing what to compare across the images.

Returns:
    The vision model's text response as a string.

Error Handling:
    - FileNotFoundError: if any image file does not exist.
    - PermissionError: if any image file is not readable.
    - ValueError: if any image format is unsupported or a file is too large.
    - VisionAPIError: if the API request fails or returns an error.""",
    input_schema=CompareImagesInput.model_json_schema(),
    annotations=ToolAnnotations(
        title="Vision Compare Images",
        read_only_hint=True,
        destructive_hint=False,
        idempotent_hint=True,
        open_world_hint=True,
    ),
)

TOOLS = [ANALYZE_TOOL, COMPARE_TOOL]


async def handle_list_tools(ctx, params=None) -> ListToolsResult:
    return ListToolsResult(tools=TOOLS)


async def handle_call_tool(ctx, params) -> CallToolResult:
    try:
        if params.name == "vision_analyze_image":
            input_model = AnalyzeImageInput(**params.arguments)
            result = await _analyze_image(input_model)
            return CallToolResult(content=[TextContent(type="text", text=result)])
        elif params.name == "vision_compare_images":
            input_model = CompareImagesInput(**params.arguments)
            result = await _compare_images(input_model)
            return CallToolResult(content=[TextContent(type="text", text=result)])
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {params.name}")],
                is_error=True,
            )
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=str(e))],
            is_error=True,
        )


async def _analyze_image(params: AnalyzeImageInput) -> str:
    content_blocks = []

    data_uri = encode_image(params.image_path)

    content_blocks.append(
        {"type": "image_url", "image_url": {"url": data_uri, "detail": "high"}}
    )
    content_blocks.append({"type": "text", "text": params.prompt})

    return await call_vision_api(content_blocks)


async def _compare_images(params: CompareImagesInput) -> str:
    content_blocks = []

    for i, path in enumerate(params.image_paths, start=1):
        data_uri = encode_image(path)

        content_blocks.append(
            {"type": "image_url", "image_url": {"url": data_uri, "detail": "high"}}
        )
        content_blocks.append({"type": "text", "text": f"Image {i}:"})

    content_blocks.append({"type": "text", "text": params.prompt})

    return await call_vision_api(content_blocks)


async def main_async():
    server = Server(
        "vision_mcp",
        on_list_tools=handle_list_tools,
        on_call_tool=handle_call_tool,
    )
    init_opts = server.create_initialization_options()
    async with stdio_server() as (read, write):
        await server.run(read, write, init_opts, raise_exceptions=True)


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
