import paho.mqtt.client as mqtt_client
import json, time
from exporter_var import *

# Function to establish a connection to the MQTT broker and subscribe to a topic
def connect_sub_mqtt():

    # Callback for successful connection to the MQTT broker
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(sub_topic) # Subscribe to the specified topic
        else:
            print("Failed to connect, return code %d\n", rc)
    
    # Callback for handling disconnection from the MQTT broker
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

            reconnect_delay *= RECONNECT_RATE # Increase delay exponentially
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1
        print("Reconnect failed after {} attempts. Exiting...".format(reconnect_count))

    # Callback for receiving messages from the MQTT broker
    def on_message(client, userdata, msg):

        print("Received data from `{}` topic".format(msg.topic))
        promethify_data(msg)  # Process the received message for Prometheus metrics

    # Initialize the MQTT client and assign the callbacks
    client = mqtt_client.Client(sub_client_id)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, sub_port)
    return client

# Function to continuously run the MQTT subscriber
def sub_client_run():
    sub_client = connect_sub_mqtt()
    sub_client.loop_forever()

# Function to publish a request message to collect data
def request_data(client):
    msg = 'Time to collect data.'
    result = client.publish(pub_topic, msg)
    status = result[0]
    if status == 0:
        print("Sent `{}` to topic `{}`".format(msg, pub_topic))
    else:
        print("Failed to send message to topic {}".format(pub_topic))

# Function to connect to the MQTT broker as a publisher
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

# Function to gather data by publishing a request message
def gather_data():
    pub_client = connect_pub_mqtt()
    pub_client.loop_start()
    request_data(pub_client)
    pub_client.loop_stop()

# Function to assign received data to Prometheus metrics
def assign_data(prom_var, data_name, sensor, jsondata):

    value =  float(jsondata[data_name].replace(',', '.')) # Parse the value
    if  value != -200:  # Exclude no readings
        prom_var.labels(sensor).set(value) # Set the metric value with sensor label  

# Function to process received MQTT messages and update Prometheus metrics
def promethify_data(msg):

    sensor = msg.topic.split('/')[1] # Extract sensor name from topic
    # Decode and parse the JSON payload
    jsondata_string = msg.payload.decode().replace("'", '"') 
    jsondata = json.loads(jsondata_string)

    # Assign each metric to the corresponding Prometheus variable
    assign_data(air_quality_co_gt_gauge, "CO(GT)", sensor, jsondata)
    assign_data(air_quality_pt08s1_co_gauge, "PT08.S1(CO)", sensor, jsondata)
    assign_data(air_quality_nmhc_gt_gauge, "NMHC(GT)", sensor, jsondata)
    assign_data(air_quality_c6h6_gt_gauge, "C6H6(GT)", sensor, jsondata)
    assign_data(air_quality_pt08s2_nmhc_gauge, "PT08.S2(NMHC)", sensor, jsondata)
    assign_data(air_quality_nox_gt_gauge, "NOx(GT)", sensor, jsondata)
    assign_data(air_quality_pt08s3_nox_gauge, "PT08.S3(NOx)", sensor, jsondata)
    assign_data(air_quality_no2_gt_gauge, "NO2(GT)", sensor, jsondata)
    assign_data(air_quality_pt08s4_no2_gauge, "PT08.S4(NO2)", sensor, jsondata)
    assign_data(air_quality_pt08s5_o3_gauge, "PT08.S5(O3)", sensor, jsondata)
    assign_data(air_quality_t_gauge, "T", sensor, jsondata)
    assign_data(air_quality_rh_gauge, "RH", sensor, jsondata)
    assign_data(air_quality_ah_gauge, "AH", sensor, jsondata)