# coding: utf-8

from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'coding.net': {
        'task': 'task.period_task',
        'schedule': crontab(minute=0, hour=1),
    },
}

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERYD_MAX_TASKS_PER_CHILD = 1
