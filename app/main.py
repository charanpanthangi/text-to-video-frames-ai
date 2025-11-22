"""Command line entrypoint for generating frames from a story."""
from __future__ import annotations

import argparse
from pathlib import Path

from .frame_generator import generate_image
from .scene_breakdown import break_story_into_scenes


def load_story(story_file: Path) -> str:
    """Read the story content from a text file."""
    if not story_file.exists():
        raise FileNotFoundError(f"Story file not found: {story_file}")
    return story_file.read_text(encoding="utf-8")


def generate_frames_from_story(story: str) -> int:
    """Generate frames for a story and return the number of scenes created."""
    scenes = break_story_into_scenes(story)
    for idx, scene in enumerate(scenes, start=1):
        print(f"[scene {idx}] {scene}")
        generate_image(scene, index=idx)
    return len(scenes)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate storyboard frames from a story.")
    parser.add_argument(
        "--story-file",
        type=Path,
        required=True,
        help="Path to a text file containing the story",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    story_text = load_story(args.story_file)
    num_scenes = generate_frames_from_story(story_text)
    print(f"Generated {num_scenes} frames in the frames/ directory.")


if __name__ == "__main__":
    main()
