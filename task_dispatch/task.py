# coding: utf-8
from __future__ import unicode_literals
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from celery import Celery
from collector.collector.crawl_agent import crawl
from django.core.mail import send_mail
from core.utils import send_html_mail

app = Celery('coding.net'.encode(), backend='redis', broker='redis://localhost:6379/0')
app.config_from_object('celery_config')


@app.task
def period_task():
    crawl()


@app.task
def send_mail_task(send_type, data=None):
    if send_type == 1 and data:
        send_html_mail(data.get('subject'), data.get('guest'), data.get('article'), data.get('recipient_list'))
    else:
        send_mail('新评论', '你有一条新评论, 登陆查看 www.rapospectre.com ', 'bluedazzle@163.com',
                  ['rapospectre@gmail.com'],
                  fail_silently=False)
