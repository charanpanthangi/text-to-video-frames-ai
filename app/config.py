"""Configuration utilities for OpenAI client setup."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables early
load_dotenv()


@dataclass(frozen=True)
class OpenAISettings:
    """Settings for interacting with OpenAI services."""

    api_key: str | None = os.getenv("OPENAI_API_KEY")
    text_model: str = os.getenv("TEXT_MODEL", "gpt-4o-mini")
    image_model: str = os.getenv("IMAGE_MODEL", "gpt-image-1")

    def client(self) -> OpenAI:
        """Return a configured OpenAI client, raising if the API key is missing."""
        if not self.api_key:
            raise EnvironmentError(
                "OPENAI_API_KEY is not set. Provide it via environment variable or .env file."
            )
        return OpenAI(api_key=self.api_key)


def get_settings() -> OpenAISettings:
    """Provide settings instance for shared use across the project."""
    return OpenAISettings()
