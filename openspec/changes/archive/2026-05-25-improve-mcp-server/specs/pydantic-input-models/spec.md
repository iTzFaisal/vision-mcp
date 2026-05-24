## ADDED Requirements

### Requirement: Tools accept validated Pydantic input models

Each MCP tool SHALL accept a single Pydantic `BaseModel` parameter that validates all input fields before the tool logic executes. FastMCP SHALL flatten the model fields so MCP clients see individual parameters (`image_path`, `prompt`, `image_paths`) rather than a nested `params` object.

#### Scenario: Analyze image with valid input

- **WHEN** a client calls `vision_analyze_image` with `image_path="/path/to/valid.png"` and `prompt="Describe this"`
- **THEN** the Pydantic model validates successfully and the tool processes the image

#### Scenario: Analyze image with empty image_path

- **WHEN** a client calls `vision_analyze_image` with `image_path=""` and `prompt="Describe this"`
- **THEN** Pydantic validation fails with a `min_length` constraint error before the tool body executes

#### Scenario: Analyze image with unknown field

- **WHEN** a client calls `vision_analyze_image` with `image_path="/path/to/valid.png"` and an extra field `extra_field="unexpected"`
- **THEN** Pydantic validation fails because `extra="forbid"` is configured

### Requirement: Pydantic model field validation constraints

The `AnalyzeImageInput` model SHALL enforce:
- `image_path`: required, `min_length=1`
- `prompt`: optional, default `"Describe this image in detail."`, `min_length=1`, `max_length=4000`

The `CompareImagesInput` model SHALL enforce:
- `image_paths`: required, `min_length=2`, `max_length=8`
- `prompt`: required, `min_length=1`, `max_length=4000`

#### Scenario: Compare images with fewer than 2 paths

- **WHEN** a client calls `vision_compare_images` with `image_paths=["single.png"]` and `prompt="Compare"`
- **THEN** Pydantic validation fails with a `min_length=2` constraint error

#### Scenario: Compare images with more than 8 paths

- **WHEN** a client calls `vision_compare_images` with 9 image paths and `prompt="Compare"`
- **THEN** Pydantic validation fails with a `max_length=8` constraint error

#### Scenario: Compare images with empty prompt

- **WHEN** a client calls `vision_compare_images` with `image_paths=["a.png", "b.png"]` and `prompt=""`
- **THEN** Pydantic validation fails with a `min_length=1` constraint error

#### Scenario: Analyze image uses default prompt when omitted

- **WHEN** a client calls `vision_analyze_image` with only `image_path="/path/to/valid.png"` (no prompt)
- **THEN** the model uses the default prompt `"Describe this image in detail."`

### Requirement: Tool naming follows service prefix convention

Each tool SHALL use a `name=` parameter in the `@mcp.tool()` decorator with the `vision_` prefix to prevent naming conflicts with other MCP servers.

#### Scenario: Tool name includes service prefix

- **WHEN** an MCP client lists available tools from this server
- **THEN** the tool names are `vision_analyze_image` and `vision_compare_images`

### Requirement: Tool annotations provide runtime hints

Each `@mcp.tool()` decorator SHALL include an `annotations=` dictionary with `title`, `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` fields to enable intelligent client decision-making.

#### Scenario: Annotations describe read-only nature

- **WHEN** an MCP client inspects tool annotations
- **THEN** both tools report `readOnlyHint: true` and `destructiveHint: false`

#### Scenario: Annotations describe external API dependency

- **WHEN** an MCP client inspects tool annotations
- **THEN** both tools report `openWorldHint: true`

### Requirement: Tool docstrings serve as descriptions

Each tool function SHALL have a comprehensive Google-style docstring that FastMCP exposes as the tool description. The docstring SHALL include sections for what the tool does, supported formats, Args, Returns, and Error Handling.

#### Scenario: Docstring appears in tool listing

- **WHEN** an MCP client retrieves tool descriptions
- **THEN** `vision_analyze_image` description includes "Analyze a single image using a vision-capable model"

#### Scenario: Docstring documents supported formats

- **WHEN** an MCP client retrieves tool descriptions
- **THEN** the description includes "Supports PNG, JPEG, GIF, and WebP formats up to 20MB"
