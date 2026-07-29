## Context

Current server uses `FastMCP` from `mcp.server.fastmcp` — a decorator-based API removed in mcp 2.0. The mcp 2.0 SDK provides two paths: `MCPServer` (high-level, decorator-based) and low-level `Server` (callback-based). See proposal.md §Why for motivation.

The server is small (2 tools, ~112 lines) with Pydantic models providing input validation.

## Goals / Non-Goals

**Goals:**
- Replace `FastMCP` with a stable mcp 2.0 API
- Preserve the exact MCP tool interface (names, schemas, annotations)
- Keep Pydantic model validation for tool inputs
- Update tests to work without FastMCP internals

**Non-Goals:**
- No behavioral changes to tool semantics
- No new features or capabilities
- No changes to config, image utils, client, or models modules (unless imports change)

## Decisions

### Decision 1: Low-level Server over MCPServer

| Criterion | Low-level Server | MCPServer (decorator) |
|---|---|---|
| Input schema | `model_json_schema()` — full Pydantic fidelity | Auto-extracted from fn params — loses minLength, maxLength |
| API shape | Flat (same as current) | Nested `$ref` when using Pydantic model params |
| Annotations | `ToolAnnotations` | `ToolAnnotations` |
| Boilerplate | More (manual callbacks) | Less (decorators) |

**Chosen: Low-level `Server` with `on_list_tools`/`on_call_tool`.**

Reasoning: MCPServer with individual params drops Pydantic field validators (the input schema loses `minLength`, `maxLength`, `description`). MCPServer with a Pydantic model param wraps arguments in `{"params": {...}}`, breaking the current API shape. The low-level Server gives full control: use `model_json_schema()` for flat schemas with all validators preserved.

### Decision 2: Error handling via `isError` flag

Current FastMCP code returns error strings as successful results. With mcp 2.0, `CallToolResult` supports `isError=True`. This is a semantic improvement — MCP clients can distinguish operational errors from successful responses.

### Decision 3: Stdio transport only

The server currently uses `mcp.run()` (default stdio). The migration uses `stdio_server()` async context manager with `asyncio.run()`. No transport changes needed since the MCP protocol is identical.

### Decision 4: Keep `analyze_image` and `compare_images` as private helpers

The current async functions implement the core logic. They'll be extracted as module-level private helpers, with `handle_call_tool` acting as the dispatch layer. This keeps the test structure largely intact.

## Risks / Trade-offs

- **[Risk] Schema equivalence**: The `model_json_schema()` output must match the current schema closely. Minor differences in JSON Schema output between Pydantic versions could cause client confusion. → Pin Pydantic implicitly via mcp 2.0's dependency range; verify schemas match by comparing serialized output.
- **[Risk] asyncio main**: Switching from blocking `mcp.run()` to `asyncio.run(stdio_server())` changes the process lifecycle. → Test by running the server and connecting an MCP client (or inspector).
- **[Trade-off] More boilerplate**: The low-level Server requires explicit `Tool` object definitions and a dispatch function, rather than two `@mcp.tool()` decorators. Acceptable given the small number of tools.

## Open Questions

None.
