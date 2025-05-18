# innovaas-mcp-server

## Project Structure

```
innovaas-mcp-server/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── mqtt_client.py
│   └── namespace_config.json
├── .env
├── .env.example
├── requirements.txt
├── service/
│   └── innovaas-mcp.service
├── README.md
├── venv/
```

- All source code and config now live in `app/`.
- `.env` and `.env.example` are for environment variables (e.g., MQTT_BROKER).
- Service file and requirements remain unchanged.

## Setup

```bash
git clone https://github.com/your-org/innovaas-mcp-server.git
cd innovaas-mcp-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and define `MQTT_BROKER`.

## Running

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Architecture

1. Receives a prompt at `/mcp`
2. Maps it to a topic using `namespace_config.json`
3. Publishes an MQTT message
4. Future: extend with LLM integration, semantic topic matching, and responses

## To Do

- [ ] Real NLP parsing
- [ ] Subscription + read support
- [ ] Model Context Protocol compliance
- [ ] Unit tests
