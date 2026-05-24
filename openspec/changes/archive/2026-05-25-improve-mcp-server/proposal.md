## Why

The vision-mcp server was audited against MCP Python best practices and found several gaps: incorrect import path, non-standard server naming, missing Pydantic input models, missing tool annotations, and minimal docstrings. These degrade client-side tool discovery and input validation, making the server less robust and harder to integrate for LLM clients.

## What Changes

- **BREAKING**: Tool parameter signatures change from individual args to a single Pydantic model parameter (`analyze_image(image_path, prompt)` → `analyze_image(params: AnalyzeImageInput)`)
- **BREAKING**: Tool names change from `analyze_image` / `compare_images` to `vision_analyze_image` / `vision_compare_images` (prefixed with `vision_`)
- Fix FastMCP import from `mcp.server` to `mcp.server.fastmcp`
- Fix server name from `"vision-mcp"` to `"vision_mcp"` (Python convention: underscores)
- Add Pydantic input models with field validation, examples, and `extra="forbid"`
- Add `name=` and `annotations=` to both `@mcp.tool()` decorators for client discovery
- Add comprehensive Google-style docstrings with Args, Returns, and Error Handling sections
- Remove manual input validation in `compare_images` (replaced by Pydantic `min_length`/`max_length`)
- Remove `DEFAULT_ANALYZE_PROMPT` module constant (default moves into Pydantic model field)

## Capabilities

### New Capabilities

- `pydantic-input-models`: Structured input models with Pydantic for both tools, providing field validation, examples, and schema generation

### Modified Capabilities

None (no existing specs to modify).

## Impact

- **Affected files**: `src/vision_mcp/server.py` (major rewrite), new `src/vision_mcp/models.py`
- **Unchanged**: `config.py`, `image_utils.py`, `client.py`, `__init__.py`
- **API**: Tool signatures and names are breaking changes for any MCP client calling these tools directly
- **Dependencies**: Pydantic is already available via the `mcp` SDK dependency chain
