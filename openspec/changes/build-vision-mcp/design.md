## Context

Claude Code communicates with MCP servers over stdio transport (newline-delimited JSON-RPC). The server runs as a child process spawned by Claude Code. This project uses Python with the `mcp` (FastMCP) library, which provides a clean decorator-based API for defining tools.

The vision model (qwen3.6-plus) exposes an OpenAI-compatible `/v1/chat/completions` endpoint. Vision images are passed as `image_url` content blocks with base64-encoded data URIs.

## Goals / Non-Goals

**Goals:**
- Two MCP tools: `analyze_image` (single image) and `compare_images` (2-8 images)
- Local file paths as input — the coding agent works with files on disk
- Configurable via environment variables (no hardcoded keys)
- Clean error messages when images are missing, unreadable, or unsupported
- Runs with `uv run server.py` — zero-install beyond `uv`

**Non-Goals:**
- URL/remote image support (first version is file-only)
- Video analysis
- Object detection with bounding boxes
- OCR-specific mode (the prompt system already supports "extract all text")
- Streaming responses
- Image generation
- Web UI or dashboard

## Decisions

### 1. Python + FastMCP over TypeScript + MCP SDK

**Choice**: Python with `mcp` (FastMCP)

**Rationale**: User preference. For a simple I/O task (read file → call API → return text), Python's minimal boilerplate wins. FastMCP decorator API is cleaner than the TypeScript SDK's imperative registration. The `httpx` library provides async HTTP with a simple API.

**Alternatives considered**: TypeScript (more verbose for this use case, all existing vision MCPs use it), Go (overkill for 2 tools).

### 2. Single-file server over module structure

**Choice**: Single `server.py` file at repo root.

**Rationale**: Two tools, one API client, ~120 lines total. A module structure (separate `tools/`, `client/`, `utils/` directories) would add complexity without real benefit. Can refactor if the tool set grows.

### 3. Async HTTP with httpx

**Choice**: `httpx.AsyncClient` for API calls.

**Rationale**: FastMCP tools can be async. Non-blocking HTTP prevents the MCP connection from stalling during slow vision model responses. `httpx` is well-maintained, supports HTTP/2, and has a simple API. No need for `aiohttp`'s extra complexity.

### 4. Base64 data URI encoding for images

**Choice**: Encode local image files as `data:image/<mime>;base64,<data>` and pass as `image_url` content blocks.

**Rationale**: The OpenAI-compatible vision API accepts images via `image_url.url` field. Pointing to `file://` URIs is not universally supported by API providers. Base64 encoding works everywhere and avoids filesystem permission issues between the MCP process and an external API.

### 5. Prompt required for compare, optional for analyze

**Choice**: `analyze_image` has an optional prompt (default: "Describe this image in detail."). `compare_images` has a required prompt.

**Rationale**: Single-image analysis has a natural default ("describe it"). Comparison has no useful default — the agent must say what to compare (differences, similarities, which is better, etc.). Making it required prevents wasteful API calls.

### 6. Image format detection via MIME type from extension

**Choice**: Map file extensions to MIME types. Support PNG, JPEG, GIF, WebP.

**Rationale**: The vision model supports these four formats. Using `mimetypes` from stdlib handles detection. BMP, TIFF, SVG are excluded (not supported by most vision models). Clear error messages tell the agent which formats are supported.

### 7. No image preprocessing (v1)

**Choice**: Send images as-is, up to a reasonable size limit (20MB).

**Rationale**: Preprocessing (resizing, compression) adds dependencies (Pillow) and complicates the flow. Most screenshots and mockups are well under 20MB. The vision model backend can handle standard sizes. Add preprocessing later if cost or performance becomes an issue.

## Risks / Trade-offs

- **API key in environment variable**: The key is passed via `.mcp.json` `env` block or the shell. Standard Claude Code pattern. Ensure `.mcp.json` uses `${VISION_API_KEY}` expansion (not hardcoded) for team sharing.
- **Large images may be slow**: No preprocessing means large images take longer and cost more tokens. Mitigation: document typical image sizes, add preprocessing in v2 if needed.
- **Vision model availability**: If opencode.ai is down or the model is overloaded, the MCP tool fails. Mitigation: clear error messages, reasonable timeout (60s default).
- **Single API call, no retry**: The server makes one HTTP call per tool invocation. No retry logic. Mitigation: the coding agent can retry by calling the tool again.
- **No conversation history**: Each call is stateless. The vision model gets no prior context. Mitigation: the agent controls prompt content and can include context in the prompt itself.

## Open Questions

- Should we add a `model` parameter override per-call? (Could switch between vision models at runtime)
- Should `compare_images` support passing one prompt per image (not just one shared prompt)?
- What timeout value? 60s seems reasonable for vision models but some large images may exceed this.
