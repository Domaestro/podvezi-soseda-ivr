## base image
FROM python:3.9-slim-buster

## install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools 
COPY requirements/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1