from datetime import timedelta
import random

BROKER_URL = 'redis://redis'
CELERY_RESULT_BACKEND = 'redis://redis'
CELERY_ACCEPT_CONTENT = ['json', 'yaml', 'pickle']
CELERYBEAT_SCHEDULE = {
    'add-every-1-minute': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=60),
        'args': (random.randint(1, 10000), random.randint(1, 10000))
    },
}
