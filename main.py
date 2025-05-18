from fastapi import FastAPI, Request
from mqtt_client import publish_message
import json

app = FastAPI()

@app.post("/mcp")
async def handle_prompt(req: Request):
    data = await req.json()
    prompt = data.get("prompt", "").lower()

    with open("namespace_config.json") as f:
        ns = json.load(f)

    # Very basic mapping logic
    if "temperature" in prompt:
        topic = "site1/line1/motor1/temp"
    else:
        topic = "default/topic"

    publish_message(topic, "Request from MCP")
    return {"status": "ok", "published_to": topic}