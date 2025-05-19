import os
import time
import random
import json
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from pathlib import Path

# Load environment variables from .env if present
load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
INTERVAL = int(os.getenv("SIM_INTERVAL", 5))  # Default to 5 seconds

CONFIG_PATH = Path(__file__).parent / "app" / "namespace_config.json"

def generate_sensor_value(tag):
    if "temp" in tag:
        return round(random.uniform(60, 100), 2)
    elif "vibration" in tag:
        return round(random.uniform(0.1, 2.0), 3)
    elif "pressure" in tag:
        return round(random.uniform(1.0, 10.0), 2)
    else:
        return round(random.uniform(0, 100), 2)

def traverse_namespace(node, path_prefix=None):
    """Recursively traverse the namespace config and yield full topic paths for all tags."""
    if path_prefix is None:
        path_prefix = []
    if isinstance(node, dict):
        for key, value in node.items():
            yield from traverse_namespace(value, path_prefix + [key])
    else:
        # Leaf node (tag)
        yield "/".join(path_prefix)

def main():
    # Load namespace config
    with open(CONFIG_PATH) as f:
        ns = json.load(f)

    # Build list of all topics to publish to
    topics = list(traverse_namespace(ns))

    print("Topics to publish:", topics)

    client = mqtt.Client()
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_HOST, MQTT_PORT, 60)

    print(f"Publishing simulated data to {len(topics)} topics every {INTERVAL} seconds.")
    try:
        while True:
            for topic in topics:
                tag = topic.split("/")[-1]
                value = generate_sensor_value(tag)
                client.publish(topic, str(value))
                print(f"Published to {topic}: {value}")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Simulator stopped.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()