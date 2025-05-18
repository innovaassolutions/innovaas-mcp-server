## Objective of This Project

To build a live simulation and working prototype of a modern industrial data architecture that demonstrates how:

🏭 **Real-world industrial environments**  
can communicate with  
🤖 **AI/LLM systems**  
through an architecture combining:  
**MCP (Model Context Protocol) + MQTT + UNS (Unified Namespace)**

---

### 👷‍♂️ In Plain Terms

You're building a working bridge between:

| From                                   | Through                                                      | To                                              |
|---------------------------------------- |-------------------------------------------------------------|-------------------------------------------------|
| Machine data, operator intent, SCADA/OT systems | An MCP server that interprets natural language + routes messages via MQTT | LLMs (like GPT), dashboards, or agents that act on it |

---

### ✅ The Goals of the Demonstration Are

- **Accept Natural Language Prompts**  
  Like: "Check temperature on Line 1" or "Start mixer 3"  
  Via a FastAPI endpoint `/mcp`

- **Translate to MQTT**  
  Prompt is processed and mapped to an MQTT topic  
  Message is published via EMQX MQTT broker

- **Visualize + Monitor the System**  
  Use MQTTX to observe data flow  
  Optionally pull into Ignition, HighByte, or a dashboard

- **Optionally Add a Real LLM (GPT or Claude)**  
  To interpret intent  
  Route messages  
  Eventually issue control logic or insights

- **Simulate a Real Unified Namespace**  
  Organize topics in a standard hierarchy (e.g., site/area/line/device/tag)  
  Enable subscription to context-aware messages

---

### 🔁 Why This Matters

This is a foundational step in letting:

- Engineers and operators issue commands in natural language
- AI make decisions based on live machine data
- A factory's Unified Namespace power predictive models, visual dashboards, or intelligent assistants

---

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

## Simulation in This Project

Currently, the simulation in this project is **on-demand** and lives in the FastAPI server:

- **Natural Language Prompts:** The `/mcp` endpoint accepts prompts (e.g., "Check temperature on Line 1") via HTTP POST.
- **Prompt-to-Topic Mapping:** Prompts are mapped to MQTT topics using simple logic and the `namespace_config.json` file.
- **MQTT Publishing:** The mapped message is published to the EMQX MQTT broker, simulating a device or system sending data/events.
- **Unified Namespace:** The topic structure in `namespace_config.json` simulates a real industrial Unified Namespace.

**What is NOT simulated (yet):**
- No automated or periodic device data publishing.
- No simulated dashboards or LLMs consuming MQTT messages.
- No time-based or event-driven simulation—actions are triggered by API calls.

**To extend the simulation:**
You can add background tasks, scripts, or services to simulate devices, dashboards, or AI agents.

## EMQX Enterprise MQTT Broker

This project uses EMQX Enterprise 5.9.0 as the MQTT broker.

- **Service name:** `emqx` (managed via systemd)
- **Dashboard:** http://localhost:18083
- **Default MQTT port:** 1883
- **License:** Free use for a single node in internal environments. See EMQX output for full license details.

To manage the broker:
```bash
sudo systemctl status emqx
sudo systemctl restart emqx
sudo systemctl stop emqx
```

## To Do

- [ ] Real NLP parsing
- [ ] Subscription + read support
- [ ] Model Context Protocol compliance
- [ ] Unit tests
