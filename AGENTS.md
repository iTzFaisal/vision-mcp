# AGENTS.md

## Project

MCP server that routes image analysis to an OpenAI-compatible vision API. Enables non-vision coding models to "see" images.

## Commands

```bash
uv sync          # install deps
uv run server    # start MCP server over stdio
```

No tests, lint, or typecheck commands are configured yet.

## Architecture

Single Python package at `src/vision_mcp/`:

| File | Role |
|---|---|
| `config.py` | Reads `VISION_API_KEY`, `VISION_API_BASE`, `VISION_MODEL` from env |
| `image_utils.py` | Validates + base64-encodes images into data URIs (PNG/JPEG/GIF/WebP, max 20MB) |
| `client.py` | Calls OpenAI-compatible `/v1/chat/completions` via httpx (60s timeout) |
| `server.py` | Exposes two MCP tools: `analyze_image` and `compare_images` via FastMCP |

Uses `FastMCP` (not the lower-level `mcp` SDK). Tools are registered via `@mcp.tool()` decorators. Server communicates over stdio (standard MCP protocol).

## Gotchas

- **`.mcp.json` is gitignored** and contains live API keys. Never read it for credentials — use `.env` or env vars.
- **`uv.lock` is gitignored** — it's intentionally not committed.
- `VISION_API_KEY` is required; `VISION_API_BASE` defaults to `https://api.openai.com/v1`, `VISION_MODEL` defaults to `gpt-4o`.
- Image paths must be local files — the server reads and encodes them, not the API.
