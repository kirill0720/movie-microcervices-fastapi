FROM python:3.11-slim

RUN apt-get update \
    && apt-get install gcc libpq-dev -y \
    && apt-get clean

WORKDIR app/

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app