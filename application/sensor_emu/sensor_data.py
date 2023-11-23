import json
import random
import os
from dotenv import load_dotenv
from paho.mqtt import client as mqtt_client

def connect_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # def on_disconnect(client, userdata, rc):
    #     logging.info("Disconnected with result code: %s", rc)
    #     reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    #     while reconnect_count < MAX_RECONNECT_COUNT:
    #         logging.info("Reconnecting in %d seconds...", reconnect_delay)
    #         time.sleep(reconnect_delay)

    #         try:
    #             client.reconnect()
    #             logging.info("Reconnected successfully!")
    #             return
    #         except Exception as err:
    #             logging.error("%s. Reconnect failed. Retrying...", err)

    #         reconnect_delay *= RECONNECT_RATE
    #         reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
    #         reconnect_count += 1
    #     logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)


    client = mqtt_client.Client(client_id)
    client.tls_set(ca_certs='./emqxsl-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    # client.on_disconnect = on_disconnect
    client.connect(broker, port)
    return client

def data_gen():
    with open("dataset.json") as datafile:
        json_data = json.load(datafile)

        randomizer = random.randint(1, len(json_data))
        #print(randomizer)
        randata = json_data[str(randomizer)]
        #print(randata)
        return randata

def publish(client, data):
    msg = f"{data}"
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Sent `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")        

### MQTT stuff

load_dotenv()
port = 8883
topic = "python/mqtt"
client_id = f'publish-sensor-test'
broker = os.environ.get("BROKER")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

if __name__ == '__main__':
    client = connect_mqtt()
    client.loop_start()
    randata = data_gen()
    publish(client, randata)
    client.loop_stop()