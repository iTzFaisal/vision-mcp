## ADDED Requirements

### Requirement: Compare multiple images
The system SHALL provide a tool that accepts 2 to 8 local image file paths and a required text prompt, sends all images simultaneously to the vision model, and returns a single text response covering the requested comparison or joint analysis.

#### Scenario: Compare two screenshots
- **WHEN** the agent calls `compare_images` with two valid PNG file paths and a prompt "What differences exist between these two screenshots?"
- **THEN** the system encodes both images as base64, sends them in a single API request with the prompt, and returns a text response describing the differences

#### Scenario: Maximum image count
- **WHEN** the agent calls `compare_images` with 8 valid image paths
- **THEN** the system sends all 8 images in a single request and returns the response

#### Scenario: Too few images
- **WHEN** the agent calls `compare_images` with only 1 image path
- **THEN** the system returns an error indicating at least 2 images are required for comparison, and suggests using `analyze_image` instead

#### Scenario: Too many images
- **WHEN** the agent calls `compare_images` with 9 or more image paths
- **THEN** the system returns an error indicating the maximum is 8 images

#### Scenario: Missing prompt
- **WHEN** the agent calls `compare_images` without a `prompt` parameter
- **THEN** the system returns an error indicating that a prompt is required

#### Scenario: One of the images is missing
- **WHEN** the agent calls `compare_images` with 3 paths where the second file does not exist
- **THEN** the system returns an error identifying which file path is invalid, without sending any API request

#### Scenario: One of the images has an unsupported format
- **WHEN** the agent calls `compare_images` where one path points to a BMP file
- **THEN** the system returns an error identifying the unsupported file and listing supported formats

### Requirement: Multi-image prompt construction
The system SHALL prepend each image in the API request with a label ("Image 1:", "Image 2:", etc.) in the prompt context to help the vision model reference specific images in its response.

#### Scenario: Images labeled in prompt
- **WHEN** the agent calls `compare_images` with 3 images
- **THEN** the system constructs a user message containing "Image 1:" followed by the first image content block, then "Image 2:" with the second, then "Image 3:" with the third, followed by the user's prompt text as the final content block

### Requirement: Shared image validation with analyze_image
The system SHALL apply the same image format validation, encoding, error handling, and API configuration checks as the `analyze_image` tool for each image in a comparison request.

#### Scenario: Consistent validation
- **WHEN** `compare_images` processes each image path
- **THEN** the same file-exists, format-support, encoding, and API error handling logic applies as documented in the `image-analysis` spec
