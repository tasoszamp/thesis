FROM python:3.11.0

WORKDIR /srv/exporter

ADD exporter.py /srv/exporter/
ADD exporter_func.py /srv/exporter/
ADD exporter_var.py /srv/exporter/
ADD requirements.txt /srv/exporter/

RUN chmod -R a+rwx /srv/exporter

RUN python3 -m pip install -r requirements.txt

EXPOSE 8000
EXPOSE 1883

ENTRYPOINT [ "gunicorn","-b", "0.0.0.0:8000", "exporter:app", "-k", "uvicorn.workers.UvicornWorker"]