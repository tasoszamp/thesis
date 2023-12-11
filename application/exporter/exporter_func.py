import paho.mqtt.client as mqtt_client
import json
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

        print("Received data from `{}` topic".format(msg.topic))
        promethify_data(msg)



    client = mqtt_client.Client(sub_client_id)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, sub_port)
    return client

def sub_client_run():
    sub_client = connect_sub_mqtt()
    sub_client.loop_forever()

def request_data(client):
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
    request_data(pub_client)
    pub_client.loop_stop()

def promethify_data(msg):

    sensor = msg.topic.split('/')[1]
    jsondata_string = msg.payload.decode().replace("'", '"')
    jsondata = json.loads(jsondata_string)

    air_quality_co_gt_gauge.labels(sensor).set(float(jsondata["CO(GT)"].replace(',', '.')))
    air_quality_pt08s1_co_gauge.labels(sensor).set(float(jsondata["PT08.S1(CO)"].replace(',', '.')))
    air_quality_nmhc_gt_gauge.labels(sensor).set(float(jsondata["NMHC(GT)"].replace(',', '.')))
    air_quality_c6h6_gt_gauge.labels(sensor).set(float(jsondata["C6H6(GT)"].replace(',', '.')))
    air_quality_pt08s2_nmhc_gauge.labels(sensor).set(float(jsondata["PT08.S2(NMHC)"].replace(',', '.')))
    air_quality_nox_gt_gauge.labels(sensor).set(float(jsondata["NOx(GT)"].replace(',', '.')))
    air_quality_pt08s3_nox_gauge.labels(sensor).set(float(jsondata["PT08.S3(NOx)"].replace(',', '.')))
    air_quality_no2_gt_gauge.labels(sensor).set(float(jsondata["NO2(GT)"].replace(',', '.')))
    air_quality_pt08s4_no2_gauge.labels(sensor).set(float(jsondata["PT08.S4(NO2)"].replace(',', '.')))
    air_quality_pt08s5_o3_gauge.labels(sensor).set(float(jsondata["PT08.S5(O3)"].replace(',', '.')))
    air_quality_t_gauge.labels(sensor).set(float(jsondata["T"].replace(',', '.')))
    air_quality_rh_gauge.labels(sensor).set(float(jsondata["RH"].replace(',', '.')))
    air_quality_ah_gauge.labels(sensor).set(float(jsondata["AH"].replace(',', '.')))