FROM python:3.14-alpine

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080

COPY ./ /app