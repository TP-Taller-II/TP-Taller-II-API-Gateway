FROM python:3.7.7-stretch
RUN apt-get update
RUN pip install poetry
WORKDIR /app
ENV POETRY_VIRTUALENVS_IN_PROJECT true
COPY poetry.lock pyproject.toml ./
RUN poetry install
COPY . .
RUN poetry install
RUN poetry run pip install gunicorn