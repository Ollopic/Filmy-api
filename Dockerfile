FROM python:3.13

RUN apt-get update

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r requirements.txt