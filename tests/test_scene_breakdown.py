from __future__ import annotations

import sys
import types
from pathlib import Path
from types import SimpleNamespace

# Provide lightweight stubs if dependencies are not installed in the environment
if "openai" not in sys.modules:
    openai_stub = types.ModuleType("openai")
    class OpenAI:  # pragma: no cover - stubbed for import compatibility
        ...
    openai_stub.OpenAI = OpenAI
    sys.modules["openai"] = openai_stub

if "dotenv" not in sys.modules:
    dotenv_stub = types.ModuleType("dotenv")
    def load_dotenv(*args, **kwargs):  # pragma: no cover - stub implementation
        return None
    dotenv_stub.load_dotenv = load_dotenv
    sys.modules["dotenv"] = dotenv_stub

# Ensure the app package is importable when running tests directly
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.scene_breakdown import break_story_into_scenes


class DummyClient:
    def __init__(self, content: str):
        self._content = content
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, *args, **kwargs):
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=self._content))]
        )


def test_break_story_into_scenes_parses_lines():
    response_text = """
    1. First scene description
    2. Second scene description
    3. Third scene description
    """
    client = DummyClient(response_text)
    scenes = break_story_into_scenes("test story", client=client)

    assert scenes[:3] == [
        "First scene description",
        "Second scene description",
        "Third scene description",
    ]
    assert len(scenes) == 20  # padded to minimum
