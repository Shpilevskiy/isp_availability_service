from datetime import timedelta

BROKER_URL = 'redis://redis'
CELERY_RESULT_BACKEND = 'redis://redis'
CELERY_ACCEPT_CONTENT = ['json', 'yaml', 'pickle']
CELERYBEAT_SCHEDULE = {
    'get-byfly-connections-data-every-5-minutes': {
        'task': 'tasks.load_byfly_data',
        'schedule': timedelta(seconds=5*60),
    },
}
