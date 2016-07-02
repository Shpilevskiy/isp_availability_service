# import logging
from parser_routines.celery import app


@app.task
def add(x, y):
    print("Tasks run with arguments {} and {}".format(x, y))
    return x + y
