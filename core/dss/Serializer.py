# coding: utf-8

from __future__ import unicode_literals

import datetime
import json

from decimal import Decimal
from django.db.models.fields.files import ImageFieldFile, FileField

from .TimeFormatFactory import TimeFormatFactory
from .Warning import remove_check

try:
    from django.db import models
    from django.db.models import manager
    from django.core.paginator import Page
    from django.db.models.query import QuerySet
    import django
except ImportError:
    raise RuntimeError('django is required in django simple serializer')


class Serializer(object):
    include_attr = []
    exclude_attr = []
    objects = []
    origin_data = None
    output_type = 'raw'
    datetime_format = 'timestamp'
    foreign = False
    many = False

    def __init__(self, data, datetime_format='timestamp', output_type='raw', include_attr=None, exclude_attr=None,
                 foreign=False, many=False, *args, **kwargs):
        if include_attr:
            self.include_attr = include_attr
        if exclude_attr:
            self.exclude_attr = exclude_attr
        self.origin_data = data
        self.output_type = output_type
        self.foreign = foreign
        self.many = many
        self.datetime_format = datetime_format
        self.time_func = TimeFormatFactory.get_time_func(datetime_format)

    def check_attr(self, attr):
        if self.exclude_attr and attr in self.exclude_attr:
            return False
        if self.include_attr and attr not in self.include_attr:
            return False
        return True

    def data_inspect(self, data):
        if isinstance(data, (QuerySet, Page, list)):
            convert_data = []
            for obj in data:
                convert_data.append(self.data_inspect(obj))
            return convert_data
        elif isinstance(data, models.Model):
            obj_dict = {}
            concrete_model = data._meta.concrete_model
            for field in concrete_model._meta.local_fields:
                if field.rel is None:
                    if self.check_attr(field.name) and hasattr(data, field.name):
                        obj_dict[field.name] = self.data_inspect(getattr(data, field.name))
                else:
                    if self.check_attr(field.name) and self.foreign:
                        obj_dict[field.name] = self.data_inspect(getattr(data, field.name))
            for field in concrete_model._meta.many_to_many:
                if self.check_attr(field.name) and self.many:
                    obj_dict[field.name] = self.data_inspect(getattr(data, field.name))
            for k, v in data.__dict__.iteritems():
                if not unicode(k).startswith('_') and k not in obj_dict.keys():
                    obj_dict[k] = self.data_inspect(v)
            return obj_dict
        elif isinstance(data, manager.Manager):
            return self.data_inspect(data.all())
        elif isinstance(data, (datetime.datetime, datetime.date, datetime.time)):
            if isinstance(data, datetime.date):
                return self.time_func(data, time_format='%Y-%m-%d')
            elif isinstance(data, datetime.time):
                return self.time_func(data, time_format='%H:%M:%S')
            return self.time_func(data)
        elif isinstance(data, (ImageFieldFile, FileField)):
            return data.name
        elif isinstance(data, Decimal):
            return float(data)
        elif isinstance(data, dict):
            obj_dict = {}
            for k, v in data.iteritems():
                if self.check_attr(k):
                    obj_dict[k] = self.data_inspect(v)
            return obj_dict
        elif isinstance(data, (unicode, str, bool, float, int, long)):
            return data
        else:
            return None

    def data_format(self):
        self.objects = self.data_inspect(self.origin_data)

    def get_values(self):
        output_switch = {'dict': self.objects,
                         'raw': self.objects,
                         'json': json.dumps(self.objects, indent=4)}
        return output_switch.get(self.output_type, self.objects)

    def __call__(self):
        self.data_format()
        return self.get_values()


def serializer(data, datetime_format='timestamp', output_type='raw', include_attr=None, exclude_attr=None,
               foreign=False, many=False, *args, **kwargs):
    s = Serializer(data, datetime_format, output_type, include_attr, exclude_attr,
                   foreign, many, *args, **kwargs)
    return s()
