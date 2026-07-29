## 1. Update dependency in pyproject.toml

- [x] 1.1 Change `"mcp[cli]"` to `"mcp[cli]>=2.0"` in `pyproject.toml`
- [x] 1.2 Run `uv lock` to regenerate lockfile with mcp 2.x
- [x] 1.3 Verify `uv sync` resolves cleanly

## 2. Rewrite server.py to use mcp 2.0 Server API

- [x] 2.1 Import `Server` from `mcp.server.lowlevel` and types from `mcp.types` (Tool, TextContent, CallToolResult, ListToolsResult, ToolAnnotations)
- [x] 2.2 Define `ANALYZE_TOOL` and `COMPARE_TOOL` as module-level `Tool` objects with schemas from `model_json_schema()` and `ToolAnnotations`
- [x] 2.3 Implement `handle_list_tools` callback returning both tools
- [x] 2.4 Implement `handle_call_tool` callback dispatching to `_analyze_image` / `_compare_images` with Pydantic validation
- [x] 2.5 Extract current `analyze_image` and `compare_images` as private helpers (keep logic identical)
- [x] 2.6 Update error handling: use `CallToolResult(isError=True, content=[TextContent(type="text", text=str(e))])` for errors instead of returning strings
- [x] 2.7 Create `main_async()` using `stdio_server()` context manager
- [x] 2.8 Update `main()` to use `asyncio.run(main_async())`
- [x] 2.9 Verify the tool schemas match the current output by comparing JSON serialization

## 3. Update tests

- [x] 3.1 Update `conftest.py` fixtures — replace `mcp_instance` with a fixture exposing `TOOLS` list or individual tool objects
- [x] 3.2 Rewrite `test_server_tools.py` to check `Tool` objects directly (name, annotations, input_schema, description) instead of `_tool_manager` internals
- [x] 3.3 Update `test_server_execution.py` imports if function names changed (e.g., `analyze_image` → `_analyze_image`)
- [x] 3.4 Run `uv run pytest` and verify all tests pass

## 4. Update opencode config (revert workaround)

- [x] 4.1 Change `opencode.json` command from `["uvx", "--with", "mcp==1.29.0", "vision-mcp-server"]` back to `["uvx", "vision-mcp-server"]`

## 5. Bump version and publish

- [x] 5.1 Bump version in `pyproject.toml` from `0.1.0` to `0.2.0`
- [x] 5.2 Run `uv build` to verify the package builds
- [x] 5.3 Run `uv publish` to push to PyPI
- [x] 5.4 Verify `uvx vision-mcp-server` works from a clean environment
