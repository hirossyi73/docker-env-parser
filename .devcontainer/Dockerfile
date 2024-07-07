FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y vim curl git
COPY ./requirements.txt /app/requirements.txt
COPY ./requirements-dev.txt /app/requirements-dev.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements-dev.txt
