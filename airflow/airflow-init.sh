#!/bin/bash

if [ ! -f /.airflow-setup-complete ]; then
  echo "Running first time setup for Airflow"

  airflow db init

  echo "Creating admin user ${ADMIN_USERNAME}"
  airflow users create \
    --username $ADMIN_USERNAME \
    --firstname $ADMIN_FIRST_NAME \
    --lastname $ADMIN_LAST_NAME \
    --role Admin \
    --email $ADMIN_EMAIL \
    --password $ADMIN_PWD

  touch /.airflow-setup-complete
else
  airflow db upgrade
fi

echo "Starting up Airflow"

airflow scheduler &
airflow webserver --port $AIRFLOW_PORT &
wait
