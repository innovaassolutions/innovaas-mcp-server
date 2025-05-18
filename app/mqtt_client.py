import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

def publish_message(topic: str, payload: str):
    try:
        client = mqtt.Client()
        if MQTT_USERNAME and MQTT_PASSWORD:
            client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.publish(topic, payload)
        client.disconnect()
        print(f"✅ Published to {topic}: {payload}")
    except Exception as e:
        print(f"❌ MQTT Publish Error: {e}")
        raise e
