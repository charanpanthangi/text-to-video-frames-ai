"""FastAPI application exposing an endpoint to generate video frames."""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .frame_generator import generate_image
from .scene_breakdown import break_story_into_scenes

app = FastAPI(title="Text to Video Frames API")


class StoryRequest(BaseModel):
    story: str


class GenerationResponse(BaseModel):
    num_scenes: int
    frames_folder: str = "frames/"


@app.post("/generate-video-frames", response_model=GenerationResponse)
async def generate_video_frames(request: StoryRequest) -> GenerationResponse:
    scenes = break_story_into_scenes(request.story)
    for idx, scene in enumerate(scenes, start=1):
        generate_image(scene, index=idx)
    return GenerationResponse(num_scenes=len(scenes))
