FROM python:3.8-buster
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./api/requirements.txt .

RUN apt update && apt upgrade -y && \
    pip install --upgrade pip && \
    pip install -r requirements.txt --upgrade
