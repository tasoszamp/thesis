import json
import random, os
import socket
import subprocess
from dotenv import load_dotenv
import paho.mqtt.client as mqtt_client

port = 1883  # Default port for MQTT communication
hostname = socket.gethostname()  # Retrieve the hostname of the current machine. Hostname is enforced by docker compose.
topic = "sensor-data/{}".format(hostname)  # Define the unique topic for publishing sensor data
client_id = 'publish-{}'.format(hostname)  # Unique client ID for MQTT connection
# broker = 'localhost'  # Uncomment this line for local broker testing
broker = 'host.docker.internal'  # Use this broker when running in a Docker environment

def connect_mqtt():
    """
    Connects to the MQTT broker and sets up the on_connect callback.
    """

    def on_connect(client, userdata, flags, rc):
        """
        Callback triggered upon connecting to the MQTT broker.
        """
        if rc == 0:
            print("Connected to MQTT Broker!")
        else: 
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect 
    client.connect(broker, port)  
    return client  

def data_gen():
    """
    Generates sensor data by selecting a random entry from a dataset.
    The selection point is controlled via an environment variable.
    """
    with open("dataset.json") as datafile:
        json_data = json.load(datafile)  # Load the dataset from the JSON file
    
        load_dotenv()  # Load environment variables from the .env file
        startpoint = int(os.getenv('STARTPOINT'))  # Get the STARTPOINT from the .env file
        # Randomize the data selection around the startpoint. Slowly moves forward in time, while keeping results semi-random and ensuring a logical history.
        randomizer = random.randint(startpoint - 2, startpoint + 3)
        while randomizer not in range(1, len(json_data)):  # Ensure the randomizer is valid
            subprocess.run(["./set_startpoint"])  # Run a script to reset the startpoint
            load_dotenv()  # Reload environment variables
            startpoint = int(os.getenv('STARTPOINT'))
            randomizer = random.randint(startpoint - 10, startpoint + 10)

        # Update the STARTPOINT in the .env file
        with open(".env", "w") as f:
            f.write("STARTPOINT={}".format(randomizer))

        randata = json_data[str(randomizer)]  # Fetch the random data entry
        return randata  # Return the selected data

def publish(client, data):
    """
    Publishes a message to the MQTT topic.
    """
    msg = str(data)  # Convert the data to a string
    result = client.publish(topic, msg)  # Publish the message to the topic
    status = result[0]  # Check the result status
    if status == 0:
        print("Sent `{}` to topic `{}`".format(msg, topic))
    else:
        print("Failed to send message to topic {}".format(topic))        

if __name__ == '__main__':
    client = connect_mqtt()  # Establish the MQTT connection
    client.loop_start()  # Start the MQTT client loop in a separate thread
    randata = data_gen()  # Generate random sensor data
    publish(client, randata)  # Publish the generated data to the topic
    client.loop_stop()  # Stop the MQTT client loop
