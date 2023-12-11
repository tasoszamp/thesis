import time
from fastapi import FastAPI, Response
from prometheus_client import generate_latest
from exporter_func import *

app = FastAPI(debug=False)

@app.get("/metrics")
def get_metrics_app():
    start_time = time.time()
    
    sub_client = connect_sub_mqtt()
    sub_client.loop_start()
    gather_data()
    time.sleep(1)
    sub_client.loop_stop()
    data = generate_latest()

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:",execution_time)
    
    return Response(content=data, media_type="text/plain")

@app.get("/")
async def root():
    return "Go to /metrics for gitlab metrics"


# Run locally -> gunicorn -b localhost:8000 exporter:app -k uvicorn.workers.UvicornWorker