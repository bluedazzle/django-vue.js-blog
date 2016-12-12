# coding: utf-8

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'coding.net': {
        'task': 'task.period_task',
        'schedule': timedelta(seconds=30),
    },
}

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERYD_MAX_TASKS_PER_CHILD = 1
