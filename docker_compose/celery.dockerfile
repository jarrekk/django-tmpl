FROM python:3.6.1
MAINTAINER Jarrekk me@jarrekk.com

ENV ENV=test
#ENV ENV=production

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    git \
    apt-utils && \
    pip install -U pip setuptools && \
    rm -rf /var/lib/apt/lists/*

ADD application/requirements /tmp/requirements
RUN pip install -r /tmp/requirements/$ENV.txt

WORKDIR /django

ENV C_FORCE_ROOT=true

CMD celery -A taskapp.celery worker -B -l info
