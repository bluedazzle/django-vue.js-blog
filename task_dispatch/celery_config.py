# coding: utf-8
import sys

sys.path.append('/Users/RaPoSpectre/PycharmProjects/RaPo3/task_dispatch/task')

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'coding.net': {
        'task': 'coding_task.period_task',
        'schedule': timedelta(seconds=30),
    },
}

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
