FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./python_packages /python_packages

RUN pip install /python_packages/*

COPY ./app /app
