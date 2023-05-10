# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /FriendsServise

ADD ./FriendsServise

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# COPY . .

# CMD ["python3", "-m", "uvicorn", "main:app", "--reload", "--host=0.0.0.0"]

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]