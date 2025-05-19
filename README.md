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

## ISA-95 Naming Convention and the Unified Namespace

This project uses the ISA-95 naming convention to structure MQTT topics in a hierarchical and standardized way, forming what is known as a Unified Namespace (UNS).

### What is ISA-95?
ISA-95 is an international standard for developing an automated interface between enterprise and control systems. It defines a consistent model for representing manufacturing operations, typically using the following hierarchy:

```
<enterprise>/<site>/<area>/<line>/<workcell>/<device>/<tag>
```

### How the Unified Namespace Leverages ISA-95
The Unified Namespace (UNS) is a central, real-time, and contextual data structure that organizes all industrial data using the ISA-95 hierarchy. In this project, all MQTT topics follow this structure, making it easy to:
- Locate and subscribe to any data point in the organization
- Maintain a single source of truth for all real-time and historical data
- Enable context-aware analytics, dashboards, and AI/LLM integrations

### Value to Project Objectives
- **Scalability:** New devices, lines, or sites can be added without changing the overall structure.
- **Interoperability:** Standardized topic names make it easy for different systems (SCADA, MES, AI, dashboards) to interact.
- **Clarity:** Anyone can understand what a topic represents just by its name.
- **Extensibility:** The structure supports future expansion, such as adding new sensors or integrating with other enterprise systems.

By leveraging ISA-95 and the Unified Namespace, this project demonstrates a modern, scalable, and future-proof approach to industrial data architecture.

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

## Device Simulator

A standalone Python script (`device_simulator.py`) is provided to simulate machines and sensors in a manufacturing environment. This script publishes realistic sensor data (e.g., temperature, vibration) to MQTT topics, making your Unified Namespace come alive for demos and testing.

### Setup

1. **Activate your virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install paho-mqtt python-dotenv
   ```

3. **(Optional) Set MQTT broker info in `.env`:**
   ```
   MQTT_HOST=localhost
   MQTT_PORT=1883
   MQTT_USERNAME=
   MQTT_PASSWORD=
   ```

### Running the Simulator

From the project root, run:
```bash
python device_simulator.py --site site1 --area areaA --line line1 --interval 5
```
- This will publish simulated data every 5 seconds for each machine and sensor.
- You can adjust the `--site`, `--area`, `--line`, and `--interval` arguments as needed.

### Extending the Simulator
- Add more machines or sensors by editing the `DEFAULT_MACHINES` list in the script.
- Simulate control commands by subscribing to control topics (future feature).
- Load configuration from a file for more complex setups.

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
- [ ] Design and implement an in-stream OEE (Overall Equipment Effectiveness) processor:
    - Calculate OEE in real time from machine and sensor data via MQTT
    - Monitor and alert on OEE thresholds
    - Publish OEE metrics to MQTT and/or store in TimescaleDB
    - Integrate with MCP and LLM to support natural language queries (e.g., "What is the current OEE for Line 1?", "Alert me if OEE drops below 85%") and alert setup

## Full Roadmap

This section outlines the planned and suggested features for this project:

- **Device Simulation**
  - Simulate multiple machines and sensors (temperature, vibration, etc.)
  - Publish realistic data to MQTT topics
  - Support for control commands and dynamic configuration

- **MCP Server (FastAPI)**
  - Accept natural language prompts via `/mcp` endpoint
  - Map prompts to MQTT topics and publish commands
  - Integrate with LLMs for advanced intent recognition and responses

- **Unified Namespace (UNS)**
  - Organize MQTT topics in a standard hierarchy (site/area/line/device/tag)
  - Enable context-aware messaging and subscriptions

- **In-Stream Processing & OEE**
  - Implement a data collector/processor to subscribe to MQTT topics
  - Calculate OEE (Overall Equipment Effectiveness) in real time
  - Monitor and alert on OEE thresholds
  - Publish OEE metrics to MQTT and/or store in TimescaleDB
  - Integrate with MCP and LLM for natural language queries and alert setup

- **TimescaleDB Integration**
  - Store historical sensor and event data
  - Enable analytics, trend analysis, and dashboarding
  - Support queries from MCP/LLM for historical context

- **Dashboards & Visualization**
  - Integrate with MQTTX, Grafana, or other tools to visualize live and historical data
  - Optionally connect to Ignition, HighByte, or other industrial platforms

- **Security & Robustness**
  - Add authentication and authorization for API and MQTT
  - Handle errors and edge cases gracefully

- **Testing & Documentation**
  - Add unit and integration tests
  - Provide example API requests, responses, and usage scenarios
  - Document extensibility for new devices, sensors, and analytics

---

This roadmap will evolve as the project grows. Contributions and suggestions are welcome!

## Enterprise Readiness Requirements

To move this project from prototype to production, the following areas must be addressed:

- **Security**
  - Implement authentication and authorization for all APIs and MQTT
  - Enforce TLS/SSL for all network traffic
  - Use secure secrets management (not just .env files)

- **Reliability & Robustness**
  - Add comprehensive error handling and logging
  - Implement health checks and monitoring
  - Ensure resilience (reconnects, retries, graceful shutdowns)

- **Scalability**
  - Design for horizontal scaling of services
  - Perform load and stress testing

- **Observability**
  - Centralize and structure logs
  - Expose system and business metrics (e.g., via Prometheus)
  - Add distributed tracing

- **Deployment & Operations**
  - Containerize all services (Docker/Kubernetes)
  - Set up CI/CD pipelines
  - Document backup and restore procedures

- **Testing & Code Quality**
  - Add unit, integration, and end-to-end tests
  - Enforce code linting and type checking
  - Conduct code reviews

- **Documentation**
  - Provide API documentation, architecture diagrams, and operational runbooks

These requirements should be addressed before considering the system for production or enterprise deployment.
