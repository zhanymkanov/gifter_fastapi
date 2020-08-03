FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y gcc git libpq-dev libmagic1 && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8

COPY requirements/ /tmp/requirements

#================================================
# Packages
#================================================
RUN pip install --upgrade pip && pip install wheel &&\
    pip install --no-cache-dir -r /tmp/requirements/dev.txt


#================================================
# Code
#================================================
COPY . /proj
RUN useradd -m -d /proj -s /bin/bash app \
    && chown -R app:app /proj/*
WORKDIR /proj
USER app
