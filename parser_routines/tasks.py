from datetime import timedelta

from celery import Celery
from celery.decorators import periodic_task

celery = Celery('tasks')
celery.config_from_object('celeryconfig')


@celery.task
def add(x, y):
    with open("test.txt", "a") as f:
        f.write("TEST\n")
    return x + y


@periodic_task(run_every=timedelta(seconds=10),
               name="test_periodic_task")
def add():
    with open("test.txt", "a") as f:
        f.write("TEST\n")
    return "RAN"
