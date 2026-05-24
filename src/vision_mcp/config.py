import os
from dataclasses import dataclass


@dataclass
class Config:
    api_base: str
    api_key: str | None
    model: str


def load_config() -> Config:
    api_key = os.environ.get("VISION_API_KEY")
    return Config(
        api_base=os.environ.get("VISION_API_BASE", "https://api.openai.com/v1"),
        api_key=api_key,
        model=os.environ.get("VISION_MODEL", "gpt-4o"),
    )
