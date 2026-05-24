## Why

Claude Code running with a non-vision coding model (e.g., Qwen3-Coder) cannot interpret images -- screenshots of UI bugs, error messages, design mockups, or charts. This forces context-switching to a vision-capable UI or manual description. We need an MCP server that routes image analysis to a separate vision-capable model (qwen3.6-plus via an OpenAI-compatible endpoint) so the agent can "see" without changing its primary model.

## What Changes

- New Python MCP server exposing vision analysis tools
- `analyze_image` tool: send a local image file with an optional prompt, receive a text description
- `compare_images` tool: send 2-8 local image files for side-by-side comparison or difference detection
- OpenAI-compatible chat completions integration using `image_url` content blocks
- Stdio transport for seamless Claude Code integration via `.mcp.json`
- Configurable via environment variables: `VISION_API_BASE`, `VISION_API_KEY`, `VISION_MODEL`

## Capabilities

### New Capabilities
- `image-analysis`: Describe a single image with an optional guiding prompt, returning text. Supports local file paths (PNG, JPEG, GIF, WebP). The agent calls this when it needs to understand any image content.
- `image-comparison`: Compare 2 to 8 images simultaneously, returning a single text response that covers differences or joint analysis. The agent calls this when comparing mockups, before/after screenshots, or reference images.

### Modified Capabilities
<!-- None - no existing specs to modify -->

## Impact

- New Python project at repo root with `pyproject.toml` and `uv.lock`
- Dependencies: `mcp` (FastMCP), `httpx` (async HTTP client)
- Runtime: `uv run` or `python` via stdio transport
- Integration: `.mcp.json` entry in consuming projects referencing the server script
- No changes to existing code or configuration
