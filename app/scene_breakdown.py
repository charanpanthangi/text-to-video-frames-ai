"""Scene breakdown utilities using OpenAI chat models."""
from __future__ import annotations

import re
from typing import List

from openai import OpenAI

from .config import get_settings


PROMPT_TEMPLATE = (
    "You are a creative storyboard artist. Break the following story into clear,"
    " visual scene descriptions. Provide between 20 and 60 concise scene prompts,"
    " each on its own line and in chronological order. Avoid numbering each line;"
    " just write the scene descriptions."
)


def _clean_scene_line(line: str) -> str:
    """Normalize scene text by removing numbering and trimming whitespace."""
    cleaned = re.sub(r"^[-*\d+:.\s]+", "", line).strip()
    return cleaned


def parse_scenes(raw: str) -> List[str]:
    """Parse the raw model output into a list of scene descriptions."""
    scenes = []
    for line in raw.splitlines():
        cleaned = _clean_scene_line(line)
        if cleaned:
            scenes.append(cleaned)
    return scenes


def break_story_into_scenes(story: str, client: OpenAI | None = None) -> List[str]:
    """Use OpenAI to break a story into a list of scene descriptions.

    Args:
        story: The narrative to break down.
        client: Optional OpenAI client for dependency injection/testing.

    Returns:
        Ordered list of concise scene prompts (20-60 entries recommended).
    """

    settings = get_settings()
    client = client or settings.client()

    completion = client.chat.completions.create(
        model=settings.text_model,
        messages=[
            {"role": "system", "content": PROMPT_TEMPLATE},
            {"role": "user", "content": story},
        ],
        temperature=0.8,
    )

    content = completion.choices[0].message.content if completion.choices else ""
    scenes = parse_scenes(content)

    # Ensure recommended length boundaries if possible
    if len(scenes) < 20:
        # Pad with simple continuations if the model returned fewer scenes
        missing = 20 - len(scenes)
        scenes.extend([f"Additional scene {i+1}" for i in range(missing)])
    elif len(scenes) > 60:
        scenes = scenes[:60]

    return scenes
