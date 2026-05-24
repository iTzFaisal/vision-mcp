## Context

The vision-mcp server currently uses bare parameter signatures (individual args to each tool), no Pydantic input models, no tool annotations, a non-canonical FastMCP import, and a server name with a hyphen. These gaps mean MCP clients get less metadata for tool discovery, input validation is manual and inconsistent, and the server doesn't follow established MCP Python conventions.

The IMPROVEMENT_PLAN_MCP.md document catalogued nine specific items to fix after auditing against MCP Python best practices.

## Goals / Non-Goals

**Goals:**
- Add Pydantic input models for both tools with field validation and schema generation
- Add `name=` and `annotations=` to `@mcp.tool()` decorators for richer client discovery
- Add comprehensive Google-style docstrings that FastMCP uses as tool descriptions
- Fix FastMCP import to canonical `mcp.server.fastmcp` path
- Fix server name from `"vision-mcp"` to `"vision_mcp"` (Python underscore convention)
- Remove manual validation now handled by Pydantic
- Remove `DEFAULT_ANALYZE_PROMPT` module constant (moved to Pydantic field default)

**Non-Goals:**
- Changing image encoding logic (`image_utils.py`)
- Changing vision API client logic (`client.py`)
- Changing configuration loading (`config.py`)
- Adding new tools or modifying API call behavior
- Adding tests (not configured yet per AGENTS.md)

## Decisions

### Pydantic input models over bare parameters

**Decision**: Each tool accepts a single Pydantic `BaseModel` parameter (`params: AnalyzeImageInput`) instead of individual `(image_path, prompt)` args.

**Rationale**: FastMCP introspects Pydantic model schemas and exposes them in the MCP tool listing, giving LLM clients structured field definitions, defaults, and validation rules. Manual validation (e.g., `if len(image_paths) < 2`) is replaced by `min_length`/`max_length` constraints that produce consistent MCP error responses.

**Alternatives considered**:
- *Keep bare params + manual validation*: Simpler for this small server but inconsistent with best practices and loses schema hints for clients.
- *Use dataclasses*: No built-in validation constraints like `min_length`, `extra="forbid"`, or `examples=`.

### Single-model parameter vs. keyword args

**Decision**: Use `async def analyze_image(params: AnalyzeImageInput) -> str` (single model param).

**Rationale**: FastMCP 2.x flattens Pydantic model fields into tool parameters for the client. The LLM sees individual `image_path` and `prompt` fields, not a nested `params` object. This is the recommended pattern per the MCP Python SDK docs.

### Tool name prefix (`vision_`)

**Decision**: Prefix tool names with `vision_` → `vision_analyze_image`, `vision_compare_images`.

**Rationale**: When this server runs alongside other MCP servers, unprefixed names like `analyze_image` could collide. The service prefix prevents conflicts and helps clients identify which server provides a tool.

### Annotation hints

**Decision**: Set `readOnlyHint=True`, `destructiveHint=False`, `idempotentHint=True`, `openWorldHint=True` on both tools.

**Rationale**: Neither tool modifies the local environment (read-only), both call an external API (open world), and repeated identical calls with the same image won't change state beyond the API call (idempotent). These hints help MCP clients decide when to call tools and how to handle errors.

### Pydantic model config

**Decision**: Use `ConfigDict(str_strip_whitespace=True, extra="forbid")`.

**Rationale**: Strips leading/trailing whitespace from string inputs to avoid common user errors. `extra="forbid"` prevents typos (e.g., `imagePath` vs `image_path`) from silently being ignored.

## Risks / Trade-offs

- **[Breaking change] Tool signatures**: Any external caller invoking `analyze_image(image_path, prompt)` directly will break → mitigated by this being an MCP tool where the client serializes parameters by name, and FastMCP flattens the Pydantic model fields so parameter names remain `image_path` and `prompt` at the wire level.
- **[Breaking change] Tool names**: `analyze_image` → `vision_analyze_image` breaks any client hardcoding the old name → mitigated by this being a development tool with no established client base.
- **[Dependency] Pydantic**: The `mcp` SDK already depends on Pydantic, so no new dependency is introduced.
