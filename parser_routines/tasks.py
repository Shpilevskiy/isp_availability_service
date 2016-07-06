from celery import Celery

from by_isp_coverage import ByflyParser

celery = Celery('tasks')
celery.config_from_object('celeryconfig')


@celery.task
def load_byfly_data():
    parser = ByflyParser()
    number_of_connections = 0

    # Add database writes here later
    for c in parser.get_connections():
        number_of_connections += 1
    msg = "{} of houses are able to have high-speed internet from ByFly."
    print(msg.format(number_of_connections))


@celery.task
def add(x, y):
    return x + y
