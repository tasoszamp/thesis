import socket
import time
import subprocess
import paho.mqtt.client as mqtt_client

port = 1883  # Default port for MQTT communication
topic = "collect-data"  # Topic to subscribe to for data collection
hostname = socket.gethostname()  # Get the hostname of the machine running this script. Machine (container) hostname is enforced later-on by docker compose 
client_id = 'subscribe-{}'.format(hostname)  # Unique client ID for MQTT connection
# broker = 'localhost'  # Uncomment this line for local broker testing
broker = 'host.docker.internal'  # Use when running in a Docker environment

def connect_mqtt():
    """
    Connects to the MQTT broker and sets up event handlers for connect, disconnect, and message events.
    """

    def on_connect(client, userdata, flags, rc):
        """
        Callback triggered upon connecting to the MQTT broker.
        """
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(topic)  # Subscribe to the specified topic
        else:
            print("Failed to connect, return code %d\n", rc)
    
    def on_disconnect(client, userdata, rc):
        """
        Callback triggered when the MQTT client disconnects from the broker.
        Implements an exponential backoff strategy for reconnection attempts.
        """
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
        """
        Callback triggered when a message is received on the subscribed topic.
        """
        print("Received `{}` from `{}` topic".format(msg.payload.decode(), msg.topic))
        subprocess.run(["./sensor_data"])  # Execute the sensor_data script upon message receipt

    # Create an MQTT client instance, assign the callback functions and connect
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, port)
    return client  # Return the configured client instance

def run():
    """
    Main function to connect the MQTT client and start its loop.
    """
    client = connect_mqtt()
    client.loop_forever()

if __name__ == '__main__':
    run()