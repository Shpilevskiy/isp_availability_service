from celery import Celery

from parser_routines import celeryconfig


app = Celery()
app.config_from_object(celeryconfig)
