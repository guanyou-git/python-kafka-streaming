FROM python:3.7-buster

COPY ./python_packages /python_packages

RUN pip install /python_packages/*

COPY ./app /app

CMD ["python","/app/main.py"]
#ENTRYPOINT ["tail","-f","dev/null"]


