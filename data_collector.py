import os
import psycopg2
import paho.mqtt.client as mqtt
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_DB = os.getenv("PG_DB", "factory")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("#")  # Subscribe to all topics

def on_message(client, userdata, msg):
    value = None
    try:
        value = float(msg.payload.decode())
    except Exception:
        print(f"Non-numeric payload on {msg.topic}: {msg.payload}")
        return
    ts = datetime.utcnow()
    cur = userdata['pg'].cursor()
    cur.execute(
        "INSERT INTO sensor_data (time, topic, value) VALUES (%s, %s, %s)",
        (ts, msg.topic, value)
    )
    userdata['pg'].commit()
    cur.close()
    print(f"Stored: {msg.topic} = {value} at {ts}")

def main():
    pg = psycopg2.connect(
        host=PG_HOST, dbname=PG_DB, user=PG_USER, password=PG_PASSWORD
    )
    client = mqtt.Client(userdata={'pg': pg})
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
