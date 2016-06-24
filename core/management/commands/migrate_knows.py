# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests

from django.core.management.base import BaseCommand
from api.models import Knowledge


class Command(BaseCommand):
    def handle(self, *args, **options):
        res = requests.get('http://www.rapospectre.com:8080/knows')
        json_data = json.loads(res.content)
        know_list = json_data.get('body').get('knows')
        for know in know_list:
            Knowledge(question=know.get('question'),
                      answer=know.get('answer'),
                      publish=True).save()
