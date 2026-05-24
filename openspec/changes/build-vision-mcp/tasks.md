## 1. Project Setup

- [x] 1.1 Initialize Python project with `pyproject.toml` (Python 3.10+, `mcp[cli]`, `httpx` dependencies)
- [x] 1.2 Create `.env.example` with `VISION_API_BASE`, `VISION_API_KEY`, `VISION_MODEL` placeholders
- [x] 1.3 Create `.gitignore` for `__pycache__`, `.env`, `.venv`, `uv.lock`, `*.pyc`

## 2. Core Infrastructure

- [x] 2.1 Implement `config.py` — read `VISION_API_BASE`, `VISION_API_KEY`, `VISION_MODEL` from env vars with defaults
- [x] 2.2 Implement `image_utils.py` — MIME type detection via file extension (stdlib `mimetypes`), base64 encoding, supported format validation (PNG, JPEG, GIF, WebP)

## 3. Vision API Client

- [x] 3.1 Implement `client.py` — async function to call OpenAI-compatible chat completions with `image_url` content blocks
- [x] 3.2 Handle API errors: non-200 responses, network errors, empty choices, connection timeouts (60s default)

## 4. MCP Tools

- [x] 4.1 Implement `analyze_image` tool — accepts `image_path` (required) and `prompt` (optional, defaults to "Describe this image in detail."), returns text response
- [x] 4.2 Implement `compare_images` tool — accepts `image_paths` (required, list of 2-8 strings) and `prompt` (required), labels images as "Image 1:", "Image 2:", etc., returns text response

## 5. MCP Server Entry Point

- [x] 5.1 Create `server.py` — FastMCP server setup, register both tools, stdio transport
- [x] 5.2 Add `pyproject.toml` scripts section so server runs with `uv run server`

## 6. Testing & Verification

- [x] 6.1 Manual test: run server via `uv run server` and verify stdio JSON-RPC handshake
- [ ] 6.2 Manual test: register with Claude Code via `claude mcp add` and test `analyze_image` with a real screenshot
- [ ] 6.3 Manual test: test `compare_images` with two screenshots
- [x] 6.4 Manual test: verify error handling for missing files, unsupported formats, and missing API key

## 7. Documentation

- [x] 7.1 Write README.md — setup instructions, env var reference, Claude Code integration example, tool descriptions
