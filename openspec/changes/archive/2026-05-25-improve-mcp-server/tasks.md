## 1. Create Pydantic Input Models

- [x] 1.1 Create `src/vision_mcp/models.py` with `AnalyzeImageInput` and `CompareImagesInput` models
- [x] 1.2 Configure `ConfigDict(str_strip_whitespace=True, extra="forbid")` on both models
- [x] 1.3 Add field descriptions, `examples=`, and validation constraints (`min_length`, `max_length`)

## 2. Update server.py

- [x] 2.1 Fix FastMCP import from `mcp.server` to `mcp.server.fastmcp`
- [x] 2.2 Fix server name from `"vision-mcp"` to `"vision_mcp"`
- [x] 2.3 Remove `DEFAULT_ANALYZE_PROMPT` module constant
- [x] 2.4 Add `name="vision_analyze_image"` and annotations to the `analyze_image` decorator
- [x] 2.5 Add `name="vision_compare_images"` and annotations to the `compare_images` decorator
- [x] 2.6 Add comprehensive Google-style docstrings to both tool functions
- [x] 2.7 Update `analyze_image` signature to accept `params: AnalyzeImageInput`
- [x] 2.8 Update `compare_images` signature to accept `params: CompareImagesInput`
- [x] 2.9 Remove manual validation from `compare_images` (now handled by Pydantic)
- [x] 2.10 Import `AnalyzeImageInput` and `CompareImagesInput` from `.models`

## 3. Add Test Coverage

- [x] 3.1 Add `pytest` and `pytest-asyncio` as dev dependencies
- [x] 3.2 Create `tests/` directory with `__init__.py`
- [x] 3.3 Create `tests/conftest.py` with fixtures for the MCP server instance
- [x] 3.4 Create `tests/test_models.py` — test Pydantic validation (valid input, empty paths, too few/many images, missing fields, extra fields, default prompt)
- [x] 3.5 Create `tests/test_server_tools.py` — test tool registration metadata (tool names, annotations, docstrings exposed via FastMCP)
- [x] 3.6 Create `tests/test_server_execution.py` — test tool execution with mocked encode_image and call_vision_api (success, file-not-found, API error paths)

## 4. Verification

- [x] 4.1 Run `uv run python -c "import vision_mcp.server; print('Imports OK')"` to verify imports
- [x] 4.2 Run `uv run pytest tests/ -v` to verify all tests pass
- [x] 4.3 Run `uv run server --help` to verify MCP server starts without errors
