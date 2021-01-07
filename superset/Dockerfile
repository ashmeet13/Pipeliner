# https://github.com/tylerFowler/docker-superset
FROM python:3.8-slim

ENV SUPERSET_HOME /superset

# Superset Server Configs
ENV SUP_WEBSERVER_WORKERS 10
ENV SUP_WEBSERVER_PORT 8088
ENV SUP_WEBSERVER_TIMEOUT 60

# Admin Auth Details
ENV ADMIN_USERNAME admin
ENV ADMIN_FIRST_NAME admin
ENV ADMIN_LAST_NAME user
ENV ADMIN_EMAIL admin@nowhere.com
ENV ADMIN_PWD superset

RUN apt-get update \
&& apt-get install -y \
  libpq-dev \
  build-essential gcc git \
  libssl-dev libffi-dev libsasl2-dev libldap2-dev

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN apt-get remove -y \
  build-essential libssl-dev libffi-dev libsasl2-dev libldap2-dev git \
&& apt-get -y autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
&& apt-get autoremove -y \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir $SUPERSET_HOME

COPY superset-init.sh /superset-init.sh
RUN chmod +x /superset-init.sh

ADD src /superset/

VOLUME $SUPERSET_HOME
EXPOSE 8088

ENTRYPOINT [ "/superset-init.sh" ]
