# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import datetime
import requests
from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone

from api.models import Article, Classification, Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        res = requests.get('http://www.rapospectre.com/migrate')
        json_data = json.loads(res.content)
        blog_list = json_data.get('body').get('blog')
        for itm in blog_list:
            if Article.objects.filter(title=itm.get('caption')).exists():
                continue
            c_name = itm.get('classification').get('c_name')
            classifi = Classification.objects.filter(title=c_name)
            if not classifi.exists():
                classifi = Classification(title=c_name).save()
            else:
                classifi = classifi[0]
            if not classifi:
                classifi = Classification.objects.all()[0]
            create_time = datetime.datetime.strptime(itm.get('create_time'), '%Y-%m-%d %H:%M:%S')
            create_time = create_time.replace(tzinfo=get_current_timezone())
            Article(title=itm.get('caption'),
                    content=itm.get('content'),
                    publish=True,
                    create_time=create_time,
                    classification=classifi,
                    views=int(itm.get('read_count'))
                    ).save()
