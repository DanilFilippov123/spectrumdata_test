FROM python:3.14-alpine

WORKDIR /app

EXPOSE 8080

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY ./ /app
RUN poetry install
