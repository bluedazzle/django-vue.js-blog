# -*- coding: utf-8 -*-

# from __future__ import absolute_import

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import sys
import os
from RaPo3.settings import BASE_DIR
sys.path.append(BASE_DIR)

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'RaPo3.settings'
django.setup()

import scrapy

from scrapy_djangoitem import DjangoItem
from api.models import Collection


class CodingItem(DjangoItem):
    django_model = Collection
    amount = scrapy.Field(default=0)
    role = scrapy.Field()
    type = scrapy.Field()
    duration = scrapy.Field()
    detail = scrapy.Field()
    extra = scrapy.Field()
