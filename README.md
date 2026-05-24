# vision-mcp

MCP server that provides vision analysis tools via an OpenAI-compatible API. Enables non-vision coding models to "see" images by routing image analysis to a separate vision-capable model.

## Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- An OpenAI-compatible vision API endpoint (e.g., OpenAI, opencode.ai, or any provider supporting `/v1/chat/completions` with `image_url` content blocks)

### Installation

```bash
git clone <repo-url>
cd vision-mcp
cp .env.example .env
# Edit .env with your API credentials
uv sync
```

### Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `VISION_API_BASE` | No | `https://api.openai.com/v1` | Base URL for the OpenAI-compatible API |
| `VISION_API_KEY` | **Yes** | — | API key for authentication |
| `VISION_MODEL` | No | `gpt-4o` | Model name to use for vision tasks |

### Run the Server

```bash
uv run server
```

The server communicates over stdio using the MCP JSON-RPC protocol.

## Tools

### `analyze_image`

Analyzes a single image file with an optional prompt.

| Parameter | Required | Description |
|---|---|---|
| `image_path` | Yes | Path to a local image file (PNG, JPEG, GIF, WebP) |
| `prompt` | No | Guiding prompt (default: "Describe this image in detail.") |

**Example:**

```
analyze_image --image_path screenshot.png --prompt "What error is shown in this screenshot?"
```

### `compare_images`

Compares 2 to 8 image files simultaneously with a required prompt.

| Parameter | Required | Description |
|---|---|---|
| `image_paths` | Yes | List of 2-8 local image file paths |
| `prompt` | Yes | Prompt describing what to compare |

**Example:**

```
compare_images --image_paths before.png after.png --prompt "What changed between these two screenshots?"
```

## Claude Code Integration

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "vision": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/vision-mcp", "server"],
      "env": {
        "VISION_API_BASE": "https://api.opencode.ai/v1",
        "VISION_API_KEY": "${VISION_API_KEY}",
        "VISION_MODEL": "qwen3.6-plus"
      }
    }
  }
}
```

## Supported Image Formats

- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- GIF (`.gif`)
- WebP (`.webp`)

Maximum file size: 20 MB.

## License

MIT
