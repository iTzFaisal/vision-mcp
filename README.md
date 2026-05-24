# vision-mcp

MCP server that provides vision analysis tools via an OpenAI-compatible API. Enables non-vision coding models to "see" images by routing image analysis to a separate vision-capable model.

## Setup

### Prerequisites

- An OpenAI-compatible vision API endpoint (e.g., OpenAI, opencode.ai, or any provider supporting `/v1/chat/completions` with `image_url` content blocks)

### Installation & Usage with uvx

The recommended way to run the server is via `uvx` — no manual installation needed:

```bash
uvx vision-mcp-server
```

Or install globally with uv:

```bash
uv tool install vision-mcp-server
vision-mcp-server
```

### Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `VISION_API_BASE` | No | `https://api.openai.com/v1` | Base URL for the OpenAI-compatible API |
| `VISION_API_KEY` | **Yes** | — | API key for authentication |
| `VISION_MODEL` | No | `gpt-4o` | Model name to use for vision tasks |

The server communicates over stdio using the MCP JSON-RPC protocol.

## Tools

### `vision_analyze_image`

Analyzes a single image file with an optional prompt.

| Parameter | Required | Description |
|---|---|---|---|
| `image_path` | Yes | Path to a local image file (PNG, JPEG, GIF, WebP) |
| `prompt` | No | Guiding prompt (default: "Describe this image in detail.") |

### `vision_compare_images`

Compares 2 to 8 image files simultaneously with a required prompt.

| Parameter | Required | Description |
|---|---|---|---|
| `image_paths` | Yes | List of 2-8 local image file paths |
| `prompt` | Yes | Prompt describing what to compare |

## Coding Agent Integration

### opencode / Claude Code

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "vision": {
      "command": "uvx",
      "args": ["vision-mcp-server"],
      "env": {
        "VISION_API_BASE": "https://api.openai.com/v1",
        "VISION_API_KEY": "${VISION_API_KEY}",
        "VISION_MODEL": "gpt-4o"
      }
    }
  }
}
```

**Note:** The server installed via `uvx`/`uv tool install` creates the entry point `vision-mcp-server` (derived from the project name `vision-mcp` and script name `server`).

## Supported Image Formats

- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- GIF (`.gif`)
- WebP (`.webp`)

Maximum file size: 20 MB.

## License

MIT
