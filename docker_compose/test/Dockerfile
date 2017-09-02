FROM python:3.6.1
MAINTAINER Jarrekk me@jarrekk.com

RUN groupadd -r django && useradd -r -g django django

RUN apt-get update && \
#    apt-get upgrade -y && \
    apt-get install -y git apt-utils && \
    pip install -U pip setuptools && \
    rm -rf /var/lib/apt/lists/*

COPY application/requirements /requirements
RUN pip install --no-cache-dir -r /requirements/test.txt && rm -rf /requirements

COPY docker_compose/production/uwsgi.ini /
COPY docker_compose/production/entrypoint.sh /
RUN pip install \
    --no-cache-dir \
#    --trusted-host pypi.douban.com \
#    --index-url http://pypi.douban.com/simple \
    -r /requirements/test.txt && \
    rm -rf /requirements

COPY application /app
RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
