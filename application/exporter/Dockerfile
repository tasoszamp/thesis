FROM python:3.10.6

WORKDIR /srv/gitlab_exporter

ADD gitlab_exporter_api.py /srv/gitlab_exporter/
ADD gitlab_exporter_func.py /srv/gitlab_exporter/
ADD gitlab_exporter_var.py /srv/gitlab_exporter/
ADD .env /srv/gitlab_exporter/
ADD requirements.txt /srv/gitlab_exporter/

RUN mkdir /srv/gitlab_exporter/tmp

RUN chmod -R a+rwx /srv/gitlab_exporter

RUN python3 -m pip install -r requirements.txt

ENV PROMETHEUS_MULTIPROC_DIR=/srv/gitlab_exporter/tmp

EXPOSE 8000

ENTRYPOINT [ "gunicorn","-b", "0.0.0.0:8000", "gitlab_exporter_api:app", "-k", "uvicorn.workers.UvicornWorker"]