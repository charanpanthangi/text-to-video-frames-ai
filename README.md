# Text to Video Frames AI

Generate cinematic storyboard frames from written stories using OpenAI's GPT models. The project reads a text story, breaks it into visual scenes, and renders each scene as an image frame saved to the `frames/` directory.

## Architecture
```
story text
   |
   v
[Scene Breakdown]
   |  (gpt-4o-mini)
   v
 list of scene prompts
   |
   v
[Frame Generator]
   |  (gpt-image-1)
   v
 image frames -> frames/frame_001.png ...
```

## Project Structure
- `app/` — core application modules (CLI, API, scene breakdown, frame generation)
- `frames/` — generated output frames
- `tests/` — pytest suite with mocked OpenAI calls
- `examples/` — sample story and descriptive documentation

## Requirements
- Python 3.10+
- OpenAI API key with access to GPT text and image models
- Dependencies (see `requirements.txt`):
  - `openai>=1.0.0`
  - `fastapi>=0.115.0`
  - `uvicorn>=0.30.0`
  - `python-dotenv>=1.0.0`
  - `pillow>=10.0.0`
  - `pytest>=8.0.0`

Install dependencies:
```bash
pip install -r requirements.txt
```

## Setting the OpenAI API Key
Set `OPENAI_API_KEY` in your environment or a `.env` file in the project root:
```bash
export OPENAI_API_KEY="sk-..."
# or create a .env file
OPENAI_API_KEY=sk-...
```

## CLI Usage
Generate frames from a story file:
```bash
python app/main.py --story-file examples/sample_story.txt
```
The command will:
1. Read the story text
2. Break it into 20–60 scene prompts
3. Generate one image per scene using the OpenAI Images API
4. Save frames to `frames/frame_001.png`, `frame_002.png`, etc.

## API Usage
Run the FastAPI server:
```bash
uvicorn app.api:app --reload
```

Send a request:
```bash
curl -X POST \
  http://127.0.0.1:8000/generate-video-frames \
  -H "Content-Type: application/json" \
  -d '{"story": "A brave explorer sails across a glowing sea..."}'
```
Response:
```json
{
  "num_scenes": 28,
  "frames_folder": "frames/"
}
```

## Example Scene Breakdown
For `examples/sample_story.txt`, the scene breakdown might look like:
- Mira sketches machinery in her seaside workshop.
- Dust motes swirl as she unrolls a hidden lighthouse blueprint.
- She assembles a glowing lens that captures whispered stories.
- Townspeople line up with books as the device hums to life.
- Thunderheads gather above the lantern festival.
- Mira rushes to finish wiring before the storm hits.
- The beacon flares, painting stories across the waves.
- Ships follow shimmering images safely into harbor.

## Example Frame Outputs
Frames are saved to `frames/` using zero-padded numbering:
- `frames/frame_001.png` — initial workshop scene
- `frames/frame_002.png` — attic discovery
- `...`
- `frames/frame_020.png` (or more) — final harbor celebration

## Future Enhancements
- Async image generation for faster processing
- Configurable number of scenes and resolution
- Automatic GIF/video assembly from frames
- Frontend viewer for previewing generated frames
- Persistent metadata (scene prompts and timestamps)

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
