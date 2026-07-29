## Why

`vision-mcp-server` v0.1.0 depends on `mcp[cli]` without a version pin. The `mcp` SDK 2.0 release removed the `fastmcp` submodule (`mcp.server.fastmcp`) which the server relies on. Running `uvx vision-mcp-server` installs the latest `mcp` (2.0.0) and crashes with `ModuleNotFoundError: No module named 'mcp.server.fastmcp'`. The current workaround (pinning `mcp==1.29.0` in the opencode config) is fragile and doesn't fix the underlying issue for other users.

We need to migrate off the removed `FastMCP` API onto the stable mcp 2.0 API so the package works correctly for all install methods.

## What Changes

- Replace `FastMCP` decorator-based server with `mcp.server.lowlevel.Server` using `on_list_tools`/`on_call_tool` callbacks
- Replace `mcp.run()` with `asyncio.run(main_async())` using `stdio_server()` context manager
- Update `pyproject.toml` dependency from `"mcp[cli]"` to `"mcp[cli]>=2.0"`
- Adapt tests to the new API (remove `_tool_manager` internals, test `Tool` objects directly)
- Improve error handling by using `CallToolResult(isError=True)` for proper MCP error signaling
- Bump version from `0.1.0` to `0.2.0` and publish to PyPI

**No breaking changes to the MCP tool interface.** Tool names (`vision_analyze_image`, `vision_compare_images`), input schemas, descriptions, and annotations remain identical. This is an internal refactoring only.

## Capabilities

### New Capabilities

(None — no new behavioral capabilities introduced.)

### Modified Capabilities

(None — the MCP tool interface is unchanged. This is a pure dependency/internal refactoring with `skip_specs: true`.)

## Impact

- **Dependencies**: `mcp` must be `>=2.0` (breaking change from the downstream perspective; consumers of the `vision_mcp` Python package may be affected if they imported `FastMCP`-related internals)
- **Entry point**: `vision-mcp-server` CLI script continues to work unchanged; same process launched via `mcp.run()` now goes through `asyncio.run(...)`
- **Tests**: ~3 test files need updating — `test_server_tools.py` (tool registration), `test_server_execution.py` (imports), `conftest.py` (fixtures)
- **publish**: Version bump to 0.2.0, fresh `uv lock`, `uv build`, `uv publish`
