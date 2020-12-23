FROM postgres:latest

COPY scripts/*.sql /docker-entrypoint-initdb.d/

RUN mkdir /data

COPY data/*.csv /data/

RUN chmod a+r /docker-entrypoint-initdb.d/*

EXPOSE 5432
