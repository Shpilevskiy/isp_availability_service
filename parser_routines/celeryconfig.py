from datetime import timedelta

BROKER_URL = 'redis://redis'
CELERY_RESULT_BACKEND = 'redis://redis'
CELERY_ACCEPT_CONTENT = ['json', 'yaml', 'pickle']
CELERYBEAT_SCHEDULE = {
    'get-byfly-connections-data-every-6-minutes': {
        'task': 'tasks.load_byfly_data',
        'schedule': timedelta(seconds=6*60),
    },
    'get-mts-connections-data-every-4-minutes': {
        'task': 'tasks.load_mts_data',
        'schedule': timedelta(seconds=4*60),
    },
    'get-flynet-connections-data-every-4-minutes': {
        'task': 'tasks.load_flynet_data',
        'schedule': timedelta(seconds=4*60),
    },
    'get-unet-connections-data-every-4-minutes': {
        'task': 'tasks.load_unet_data',
        'schedule': timedelta(seconds=4*60),
    },
    'get-atlant-connections-data-every-3-minutes': {
        'task': 'tasks.load_atlant_data',
        'schedule': timedelta(seconds=3*60),
    },
}
