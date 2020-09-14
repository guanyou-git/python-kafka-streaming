FROM python:3.7-buster

COPY ./python_packages /python_packages

RUN pip download confluent-kafka

#RUN pip install /python_packages/*

COPY ./app /app
