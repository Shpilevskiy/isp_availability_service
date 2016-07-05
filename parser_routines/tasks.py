from celery import Celery

celery = Celery('tasks')
celery.config_from_object('celeryconfig')


@celery.task
def add(x, y):
    return x + y
