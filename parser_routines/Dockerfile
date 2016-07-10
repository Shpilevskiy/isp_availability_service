# FROM python:3.5
FROM ubuntu:16.04

# Install 2 versions of python and extra dependencies for lxml package
RUN apt-get update; apt-get install -y python3  python3-pip python python-pip\
                                       git libevent-dev libpython3.5-dev libpq-dev
#ADD . /app/parser_routines/
WORKDIR /app/parser_routines/
ADD requirements.txt /app/parser_routines/requirements.txt

RUN python3 -m pip install -r requirements.txt
RUN python2 -m pip install supervisor

RUN mkdir -p /var/log/supervisor /var/log/celery

COPY ./conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./conf/celerybeat.conf /etc/supervisor/conf.d/celerybeat.conf
COPY ./conf/celeryd.conf /etc/supervisor/conf.d/celeryd.conf

RUN adduser --disabled-password --gecos '' workeruser

# We need to make sure all of the required tables are created in the database and celery beat and worker are launched
CMD ["bash", "-c", "python3 /app/parser_routines/create_db_tables.py && supervisord -c /etc/supervisor/conf.d/supervisord.conf"]
