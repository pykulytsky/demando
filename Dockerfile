FROM python:3.8.5-slim

RUN  apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY . /app/
