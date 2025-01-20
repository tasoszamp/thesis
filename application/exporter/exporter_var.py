from prometheus_client import Gauge

sub_port = 1883 # Port for the subscriber
pub_port = 1883 # Port for the publisher
sub_topic = "sensor-data/#" # Subscription topic for sensor data (wildcard for all subtopics)
pub_topic = "collect-data" # Topic to publish data collection requests
sub_client_id = 'subscribe-exporter' # Client ID for the MQTT subscriber
pub_client_id = 'publish-exporter' # Client ID for the MQTT publisher
#broker = 'localhost' # uncomment for local testing
broker = 'host.docker.internal' # Docker-specific hostname for connecting to the broker


# Prometheus metrics definitions
# Each metric is defined as a Prometheus Gauge with a description and a label for 'sensor'

air_quality_co_gt_gauge = Gauge('air_quality_co_gt_gauge', 'True hourly averaged concentration CO in mg/m^3 (reference analyzer)', ['sensor'])

air_quality_pt08s1_co_gauge = Gauge('air_quality_pt08s1_co_gauge', 'Tin oxide hourly averaged sensor response (nominally CO targeted)', ['sensor'])

air_quality_nmhc_gt_gauge = Gauge('air_quality_nmhc_gt_gauge', 'True hourly averaged overall Non Metanic HydroCarbons concentration in microg/m^3 (reference analyzer)', ['sensor'])

air_quality_c6h6_gt_gauge = Gauge('air_quality_c6h6_gt_gauge', 'True hourly averaged Benzene concentration in microg/m^3 (reference analyzer)', ['sensor'])

air_quality_pt08s2_nmhc_gauge = Gauge('air_quality_pt08s2_nmhc_gauge', 'Titania hourly averaged sensor response (nominally NMHC targeted)', ['sensor'])

air_quality_nox_gt_gauge = Gauge('air_quality_nox_gt_gauge', 'True hourly averaged NOx concentration in ppb (reference analyzer)', ['sensor'])

air_quality_pt08s3_nox_gauge = Gauge('air_quality_pt08s3_nox_gauge', 'Tungsten oxide hourly averaged sensor response (nominally NOx targeted)', ['sensor'])

air_quality_no2_gt_gauge = Gauge('air_quality_no2_gt_gauge', 'True hourly averaged NO2 concentration in microg/m^3 (reference analyzer)', ['sensor'])

air_quality_pt08s4_no2_gauge = Gauge('air_quality_pt08s4_no2_gauge', 'Tungsten oxide hourly averaged sensor response (nominally NO2 targeted)', ['sensor'])

air_quality_pt08s5_o3_gauge = Gauge('air_quality_pt08s5_o3_gauge', 'Indium oxide hourly averaged sensor response (nominally O3 targeted)', ['sensor'])

air_quality_t_gauge = Gauge('air_quality_t_gauge', 'Temperature in C', ['sensor'])

air_quality_rh_gauge = Gauge('air_quality_rh_gauge', 'Relative Humidity (%)', ['sensor'])

air_quality_ah_gauge = Gauge('air_quality_ah_gauge', 'Absolute Humidity', ['sensor'])