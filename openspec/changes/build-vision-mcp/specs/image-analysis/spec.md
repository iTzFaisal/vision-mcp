## ADDED Requirements

### Requirement: Analyze a single image
The system SHALL provide a tool that accepts a local image file path and an optional text prompt, sends the image to a configurable OpenAI-compatible vision model, and returns the model's text response.

#### Scenario: Analyze with default prompt
- **WHEN** the agent calls `analyze_image` with only an `image_path` parameter pointing to a valid PNG file
- **THEN** the system reads the file, encodes it as base64, sends it to the vision model with the default prompt "Describe this image in detail.", and returns the text description

#### Scenario: Analyze with custom prompt
- **WHEN** the agent calls `analyze_image` with an `image_path` and a `prompt` of "What error message is shown in this screenshot?"
- **THEN** the system sends the image with the custom prompt and returns the model's focused response about the error message

#### Scenario: Image file not found
- **WHEN** the agent calls `analyze_image` with a path to a file that does not exist
- **THEN** the system returns an error message indicating the file was not found, including the attempted path

#### Scenario: Unsupported image format
- **WHEN** the agent calls `analyze_image` with a path to a BMP or SVG file
- **THEN** the system returns an error message listing the supported formats (PNG, JPEG, GIF, WebP)

#### Scenario: API call fails
- **WHEN** the vision model API returns a non-200 status code or a network error occurs
- **THEN** the system returns an error message with the HTTP status code and response body, or a connection error description

#### Scenario: Missing API configuration
- **WHEN** the `VISION_API_KEY` environment variable is not set
- **THEN** the system returns an error message indicating that the API key is not configured

### Requirement: Image input format handling
The system SHALL accept PNG, JPEG, GIF, and WebP image files, detect the MIME type from the file extension, and encode the file contents as a base64 data URI for the vision API.

#### Scenario: PNG image encoding
- **WHEN** the agent provides a `.png` file
- **THEN** the system encodes it as `data:image/png;base64,<data>` and includes it in the API request as an `image_url` content block

#### Scenario: JPEG image encoding
- **WHEN** the agent provides a `.jpg` or `.jpeg` file
- **THEN** the system encodes it as `data:image/jpeg;base64,<data>`

#### Scenario: Filesystem read error
- **WHEN** the file exists but cannot be read due to permissions
- **THEN** the system returns an error indicating the file is not readable

### Requirement: Vision API integration
The system SHALL construct an OpenAI-compatible chat completion request containing the base64-encoded image and prompt, using the configured API base URL, API key, and model name from environment variables.

#### Scenario: Successful API response
- **WHEN** the vision API returns a 200 response with chat completion choices
- **THEN** the system extracts the first choice's message content and returns it as plain text

#### Scenario: API response has no choices
- **WHEN** the vision API returns 200 but with an empty choices array
- **THEN** the system returns an error indicating the model produced no response

### Requirement: Configuration via environment variables
The system SHALL read its configuration from environment variables at startup: `VISION_API_BASE` (default: `https://api.openai.com/v1`), `VISION_API_KEY` (required), and `VISION_MODEL` (default: `gpt-4o`).

#### Scenario: All variables configured
- **WHEN** `VISION_API_BASE`, `VISION_API_KEY`, and `VISION_MODEL` are all set
- **THEN** the system uses the provided values for API requests

#### Scenario: Using defaults
- **WHEN** only `VISION_API_KEY` is set
- **THEN** the system uses the default base URL and default model name

#### Scenario: Missing required key
- **WHEN** `VISION_API_KEY` is not set and a tool is invoked
- **THEN** the tool returns an error without making an API call
