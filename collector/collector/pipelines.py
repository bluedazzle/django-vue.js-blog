# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
from django.utils.timezone import get_current_timezone
from scrapy.exceptions import DropItem

from api.models import Collection


class CodingDuplicatesPipeline(object):
    def process_item(self, item, spider):
        collect = Collection.objects.filter(unique_id=item['unique_id'])
        if not collect.exists():
            return item
        raise DropItem('Duplicate item found')


class CodingPriorityPipeline(object):
    keywords = ['python', 'django']
    roles = ['全栈开发', '开发团队', '后端开发', '前端开发']

    def process_role(self, role):
        for itm in self.roles:
            if itm in role:
                return True
        return False

    def process_item(self, item, spider):
        extra = unicode(item['extra'])
        for itm in self.keywords:
            if itm in extra:
                item['priority'] = 3
                return item
        item['priority'] = 2 if self.process_role(item['role']) else 1
        item['time'] = datetime.datetime.now(tz=get_current_timezone())
        item.save()
        return item
