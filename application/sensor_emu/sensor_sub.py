import socket
import time
import subprocess
import paho.mqtt.client as mqtt_client

port = 1883
topic = "collect-data"
hostname = socket.gethostname()
client_id = 'subscribe-{}'.format(hostname)
#broker = 'localhost'
broker = 'host.docker.internal'

def connect_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(topic)
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
        subprocess.run(["./sensor_data"])


    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, port)
    return client

def run():
    client = connect_mqtt()
    #subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()