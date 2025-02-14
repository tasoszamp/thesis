FROM python:3.11.0

# Set the working directory inside the container
WORKDIR /srv/exporter

# Add the main application and supporting scripts to the working directory
ADD exporter.py /srv/exporter/
ADD exporter_func.py /srv/exporter/
ADD exporter_var.py /srv/exporter/
ADD requirements.txt /srv/exporter/

# Set execute permissions for all users on the project directory
RUN chmod -R a+x /srv/exporter

# Install the Python dependencies specified in requirements.txt
RUN python3 -m pip install -r requirements.txt

# Expose the necessary ports for the Prometheus metrics endpoint and the MQTT protocol
EXPOSE 8000
EXPOSE 1883

# Set the entrypoint command to run the application using Gunicorn with Uvicorn workers
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:8000", "exporter:app", "-k", "uvicorn.workers.UvicornWorker" ]
