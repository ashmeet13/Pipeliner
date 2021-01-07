FROM python:3.8-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update \
&& apt-get autoremove -y \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir /src

COPY ./src/ /src

ENTRYPOINT ["python", "-m", "src.generate_orders"]
