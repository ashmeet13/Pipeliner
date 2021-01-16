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

RUN mkdir /tests
COPY ./tests/ tests

COPY ./airflow_init_db.sh /airflow_init_db.sh
RUN chmod +x /airflow_init_db.sh

RUN /airflow_init_db.sh

COPY ./airflow_start.sh /airflow_start.sh
RUN chmod +x /airflow_start.sh

ENTRYPOINT [ "/airflow-init.sh" ]
