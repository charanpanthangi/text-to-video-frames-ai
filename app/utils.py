"""Shared utility helpers for the project."""
from __future__ import annotations

from pathlib import Path


def ensure_frames_dir(path: Path) -> None:
    """Ensure the frames directory exists."""
    path.mkdir(parents=True, exist_ok=True)
