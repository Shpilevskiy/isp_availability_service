# FROM python:3.5
FROM ubuntu:16.04

RUN apt-get update; apt-get install -y python3 python python3-pip python-pip git
ADD . /app/parser_routines/
WORKDIR /app/parser_routines/
RUN python3 -m pip install -r requirements.txt
RUN python2 -m pip install supervisor

RUN mkdir -p /var/log/supervisor /var/log/celery

COPY ./conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./conf/celerybeat.conf /etc/supervisor/conf.d/celerybeat.conf
COPY ./conf/celeryd.conf /etc/supervisor/conf.d/celeryd.conf

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
