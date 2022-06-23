FROM python:3.8.1-slim

RUN  apt-get update && apt-get install --no-install-recommends -y gcc python3-dev postgresql-server-dev-11 && rm -rf /var/lib/{apt,dpkg,cache,log}/

RUN pip install poetry==1.1.5

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY /src/scripts /app/src/scripts/
COPY README.md README.md

RUN poetry install

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/

RUN poetry -v

CMD poetry run prod
