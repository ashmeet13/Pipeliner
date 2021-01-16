#!/bin/bash

echo "Starting up Airflow"

airflow scheduler &
airflow webserver --port $AIRFLOW_PORT &
wait
