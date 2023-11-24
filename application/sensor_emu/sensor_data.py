import json
import random
import socket
from paho.mqtt import client as mqtt_client

port = 1883
hostname = socket.gethostname()
topic = f"sensor-data/{hostname}"
client_id = f'publish-{hostname}'
broker = 'localhost'
#broker = 'host.docker.internal'

def connect_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def data_gen():
    with open("dataset.json") as datafile:
        json_data = json.load(datafile)

        randomizer = random.randint(1, len(json_data))
        randata = json_data[str(randomizer)]
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