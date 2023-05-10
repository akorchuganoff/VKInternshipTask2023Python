# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
COPY . /code/