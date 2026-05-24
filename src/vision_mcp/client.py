import httpx
from .config import load_config

DEFAULT_TIMEOUT = 60.0


class VisionAPIError(Exception):
    pass


async def call_vision_api(
    content_blocks: list[dict],
    timeout: float = DEFAULT_TIMEOUT,
) -> str:
    config = load_config()

    if not config.api_key:
        raise VisionAPIError(
            "VISION_API_KEY environment variable is not set. "
            "Set it to your OpenAI-compatible API key."
        )

    messages = [
        {
            "role": "user",
            "content": content_blocks,
        }
    ]

    url = f"{config.api_base.rstrip('/')}/chat/completions"

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                url,
                json={
                    "model": config.model,
                    "messages": messages,
                    "max_tokens": 4096,
                },
                headers={
                    "Authorization": f"Bearer {config.api_key}",
                    "Content-Type": "application/json",
                },
            )
    except httpx.TimeoutException:
        raise VisionAPIError(
            f"Request timed out after {timeout} seconds. "
            "The vision model may be overloaded or the image is too large."
        )
    except httpx.RequestError as e:
        raise VisionAPIError(f"Network error calling vision API: {e}")

    if response.status_code != 200:
        raise VisionAPIError(
            f"Vision API returned status {response.status_code}: {response.text}"
        )

    data = response.json()
    choices = data.get("choices")
    if not choices or len(choices) == 0:
        raise VisionAPIError("Vision API returned no choices in response")

    message = choices[0].get("message", {})
    content = message.get("content")
    if not content:
        raise VisionAPIError("Vision API returned empty response content")

    return content
