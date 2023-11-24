import json
import random
# import os
# from dotenv import load_dotenv
from paho.mqtt import client as mqtt_client

# load_dotenv()
# port = 8883
port = 1883
topic = "python/mqtt"
client_id = f'publish-sensor-test'
broker = '127.0.0.1'
# broker = os.environ.get("BROKER")
# username = os.environ.get("USERNAME")
# password = os.environ.get("PASSWORD")

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def connect_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.tls_set(ca_certs='./emqxsl-ca.crt')
    #client.username_pw_set(username, password)
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

if __name__ == '__main__':
    client = connect_mqtt()
    client.loop_start()
    randata = data_gen()
    publish(client, randata)
    client.loop_stop()