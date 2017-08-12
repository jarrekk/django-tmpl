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

CMD mkdir -p /var/log/uwsgi

ADD docker_compose/uwsgi.ini /tmp/uwsgi.ini
CMD uwsgi /tmp/uwsgi.ini
