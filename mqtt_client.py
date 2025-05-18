import paho.mqtt.publish as publish
import os

def publish_message(topic, message):
    broker = os.getenv("MQTT_BROKER", "localhost")
    publish.single(topic, payload=message, hostname=broker)