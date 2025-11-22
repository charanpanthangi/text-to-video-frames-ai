"""Frame generation utilities using OpenAI image models."""
from __future__ import annotations

import base64
from pathlib import Path
from typing import Optional

from openai import OpenAI

from .config import get_settings
from .utils import ensure_frames_dir

FRAMES_DIR = Path("frames")


def _next_frame_path(index: Optional[int] = None) -> Path:
    """Determine the next frame file path, optionally using a provided index."""
    ensure_frames_dir(FRAMES_DIR)
    if index is not None and index > 0:
        number = index
    else:
        existing = sorted(FRAMES_DIR.glob("frame_*.png"))
        number = len(existing) + 1
    filename = f"frame_{number:03d}.png"
    return FRAMES_DIR / filename


def generate_image(
    scene_text: str,
    *,
    index: int | None = None,
    size: str = "1024x1024",
    client: OpenAI | None = None,
) -> bytes:
    """Generate an image for the provided scene and save it to the frames folder.

    Args:
        scene_text: Prompt describing the scene.
        index: Optional index for deterministic naming (1-based).
        size: Image resolution ("512x512" or "1024x1024").
        client: Optional OpenAI client for dependency injection/testing.

    Returns:
        The raw image bytes that were written to disk.
    """

    settings = get_settings()
    client = client or settings.client()

    response = client.images.generate(
        model=settings.image_model,
        prompt=scene_text,
        size=size,
        response_format="b64_json",
    )

    b64_data = response.data[0].b64_json
    image_bytes = base64.b64decode(b64_data)

    frame_path = _next_frame_path(index)
    frame_path.write_bytes(image_bytes)

    return image_bytes
