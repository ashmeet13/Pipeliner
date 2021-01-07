#!/bin/bash

export FLASK_APP=superset

if [ ! -f $SUPERSET_HOME/.setup-complete ]; then
  echo "Running first time setup for Superset"

  echo "Creating admin user ${ADMIN_USERNAME}"
  /usr/local/bin/flask fab create-admin \
    --username $ADMIN_USERNAME \
    --firstname $ADMIN_FIRST_NAME \
    --lastname $ADMIN_LAST_NAME \
    --email $ADMIN_EMAIL \
    --password $ADMIN_PWD

  echo "Initializing database"
  superset db upgrade

  echo "Creating default roles and permissions"
  superset init

  touch $SUPERSET_HOME/.setup-complete
else
  superset db upgrade
fi

echo "Starting up Superset gunicorn server"
gunicorn \
      -w ${SUP_WEBSERVER_WORKERS} \
      -k gevent \
      --timeout ${SUP_WEBSERVER_TIMEOUT} \
      -b  0.0.0.0:${SUP_WEBSERVER_PORT} \
      "superset.app:create_app()"
