from celery import Celery

celery = Celery('tasks')
celery.config_from_object('celeryconfig')


@celery.task
def add(x, y):
    with open("test.txt", "a") as f:
        f.write("TEST\n")
    return x + y
