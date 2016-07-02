from datetime import timedelta

BROKER_URL = 'redis://redis'
CELERY_RESULT_BACKEND = 'redis://redis'
CELERY_ACCEPT_CONTENT = ['json', 'yaml', 'pickle']
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'parser_routines.tasks.add',
        'schedule': timedelta(seconds=30),
        'args': (16, 16)
    },
}
