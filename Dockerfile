FROM python:3.14-alpine

WORKDIR /app

EXPOSE 8080

COPY ./ /app
RUN pip install poetry && poetry install