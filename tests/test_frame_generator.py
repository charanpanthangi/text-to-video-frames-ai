from __future__ import annotations

import base64
import sys
import types
from pathlib import Path
from types import SimpleNamespace

import pytest

# Provide lightweight stubs if dependencies are not installed in the environment
if "openai" not in sys.modules:
    openai_stub = types.ModuleType("openai")
    class OpenAI:  # pragma: no cover - stub for import compatibility
        ...
    openai_stub.OpenAI = OpenAI
    sys.modules["openai"] = openai_stub

if "dotenv" not in sys.modules:
    dotenv_stub = types.ModuleType("dotenv")
    def load_dotenv(*args, **kwargs):  # pragma: no cover - stub implementation
        return None
    dotenv_stub.load_dotenv = load_dotenv
    sys.modules["dotenv"] = dotenv_stub

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app.frame_generator as fg


class DummyImageData:
    def __init__(self, b64_json: str):
        self.b64_json = b64_json


class DummyImages:
    def __init__(self, b64_json: str):
        self._b64 = b64_json

    def generate(self, *args, **kwargs):
        return SimpleNamespace(data=[DummyImageData(self._b64)])


class DummyClient:
    def __init__(self, b64_json: str):
        self.images = DummyImages(b64_json)


@pytest.fixture
def tmp_frames_dir(tmp_path: Path):
    original_dir = fg.FRAMES_DIR
    fg.FRAMES_DIR = tmp_path
    yield tmp_path
    fg.FRAMES_DIR = original_dir


def test_generate_image_saves_file(tmp_frames_dir: Path):
    pixel = base64.b64encode(b"fake image bytes").decode("utf-8")
    client = DummyClient(pixel)

    output = fg.generate_image("a scene", index=1, client=client)

    expected_path = tmp_frames_dir / "frame_001.png"
    assert expected_path.exists()
    assert output == b"fake image bytes"
