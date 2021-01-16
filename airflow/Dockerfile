FROM python:3.8-slim

ENV AIRFLOW_HOME /airflow

ENV ADMIN_USERNAME admin
ENV ADMIN_FIRST_NAME admin
ENV ADMIN_LAST_NAME user
ENV ADMIN_EMAIL admin@nowhere.com
ENV ADMIN_PWD admin
ENV AIRFLOW__CORE__LOAD_EXAMPLES False

ENV AIRFLOW_PORT 8089

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir $AIRFLOW_HOME

RUN mkdir $AIRFLOW_HOME/dags
COPY ./dags/ $AIRFLOW_HOME/dags

COPY /airflow-init.sh /airflow-init.sh
RUN chmod +x /airflow-init.sh

ENTRYPOINT [ "/airflow-init.sh" ]
