FROM python:3.12-slim-bullseye

RUN pip install poetry==1.8.2
RUN apt-get update && apt-get -y install git

WORKDIR /app

COPY ./pyproject.toml pyproject.toml
COPY ./poetry.lock poetry.lock
RUN poetry config virtualenvs.create false && poetry install --only main --no-root --no-cache

ADD . .

CMD ./main.py