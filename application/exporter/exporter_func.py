import paho.mqtt.client as mqtt_client
import subprocess
from exporter_var import *

def connect_sub_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(sub_topic)
        else:
            print("Failed to connect, return code %d\n", rc)
    
    def on_disconnect(client, userdata, rc):

        FIRST_RECONNECT_DELAY = 1
        RECONNECT_RATE = 2
        MAX_RECONNECT_COUNT = 12
        MAX_RECONNECT_DELAY = 60

        print("Disconnected with result code: %s", rc)
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            print("Reconnecting in {} seconds...".format(reconnect_delay))
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                print("Reconnected successfully!")
                return
            except Exception as err:
                print("{}. Reconnect failed. Retrying...".format(err))

            reconnect_delay *= RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1
        print("Reconnect failed after {} attempts. Exiting...".format(reconnect_count))

    def on_message(client, userdata, msg):

        print("Received `{}` from `{}` topic".format(msg.payload.decode(), msg.topic))


    client = mqtt_client.Client(sub_client_id)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, sub_port)
    return client

def sub_client_run():
    sub_client = connect_sub_mqtt()
    sub_client.loop_forever()

def publish(client):
    msg = 'Time to collect data.'
    result = client.publish(pub_topic, msg)
    status = result[0]
    if status == 0:
        print("Sent `{}` to topic `{}`".format(msg, pub_topic))
    else:
        print("Failed to send message to topic {}".format(pub_topic))

def connect_pub_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(pub_client_id)
    client.on_connect = on_connect
    client.connect(broker, pub_port)
    return client

def gather_data():
    pub_client = connect_pub_mqtt()
    pub_client.loop_start()
    publish(pub_client)
    pub_client.loop_stop()
