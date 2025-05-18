from fastapi import FastAPI
from pydantic import BaseModel
from .mqtt_client import publish_message
import json
from pathlib import Path
import os

app = FastAPI()

# Define the expected request model
class PromptInput(BaseModel):
    prompt: str

@app.post("/mcp")
async def handle_prompt(payload: PromptInput):
    prompt = payload.prompt.lower()

    config_path = Path(__file__).parent / "namespace_config.json"
    with open(config_path) as f:
        ns = json.load(f)

    # Very basic mapping logic
    if "temperature" in prompt:
        topic = "site1/line1/motor1/temp"
    else:
        topic = "default/topic"

    publish_message(topic, "Request from MCP")
    return {"status": "ok", "published_to": topic}
