# coding: utf-8
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from celery import Celery
from collector.collector.crawl_agent import crawl

app = Celery('coding.net', backend='redis', broker='redis://localhost:6379/0')
app.config_from_object('celery_config')


@app.task
def period_task():
    crawl()
