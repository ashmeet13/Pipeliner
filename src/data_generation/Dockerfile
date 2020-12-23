FROM python:3.7-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt
RUN mkdir /src

COPY ./src/ /src

# RUN ["chmod", "+x", "/src/wait-for-postgres.sh"]

ENTRYPOINT ["python", "-m", "src.generate_orders"]
