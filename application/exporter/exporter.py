import time
from fastapi import FastAPI, Response
from prometheus_client import generate_latest
from exporter_func import *

app = FastAPI(debug=False)

# Define an endpoint to serve metrics
@app.get("/metrics")
def get_metrics_app():
    start_time = time.time()
    
    # Connect to MQTT and start collecting data
    sub_client = connect_sub_mqtt()
    sub_client.loop_start()
    gather_data()
    time.sleep(1) # Allow time for data collection, in case sensors take time to respond
    sub_client.loop_stop()

    # Generate metrics data in Prometheus format
    data = generate_latest()

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:",execution_time)

    # Return the metrics data as a plain text HTTP response
    return Response(content=data, media_type="text/plain")

# Define a root endpoint with a simple message
@app.get("/")
async def root():
    return "Go to /metrics for gitlab metrics"

# Note for running the application locally
# Use the command:
# gunicorn -b localhost:8000 exporter:app -k uvicorn.workers.UvicornWorker