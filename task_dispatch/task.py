# coding: utf-8
import sys

sys.path.append('/Users/RaPoSpectre/PycharmProjects/RaPo3/')

from celery import Celery
from collector.collector.crawl_agent import crawl

app = Celery('coding.net', backend='redis', broker='redis://localhost:6379/0')
app.config_from_object('celery_config')


@app.task
def period_task():
    crawl()
