# coding: utf-8

import time
from functools import partial

try:
    from django.utils import timezone
except ImportError:
    raise RuntimeError('Django is required for django simple serializer.')


class TimeFormatFactory(object):
    def __init__(self):
        super(TimeFormatFactory, self).__init__()

    @staticmethod
    def datetime_to_string(datetime_time, time_format='%Y-%m-%d %H:%M:%S'):
        if not hasattr(datetime_time, 'tzinfo'):
            return datetime_time.strftime('%Y-%m-%d')
        if datetime_time.tzinfo is None:
            return datetime_time.strftime(time_format)
        datetime_time = datetime_time.astimezone(timezone.get_current_timezone())
        return datetime_time.strftime(time_format)

    @staticmethod
    def datetime_to_timestamp(datetime_time):
        if not hasattr(datetime_time, 'tzinfo'):
            return time.mktime(datetime_time.timetuple())
        if datetime_time.tzinfo is None:
            return time.mktime(datetime_time.timetuple())
        datetime_time = datetime_time.astimezone(timezone.get_current_timezone())
        return time.mktime(datetime_time.timetuple())

    @staticmethod
    def get_time_func(func_type='string', time_format='%Y-%m-%d %H:%M:%S'):
        if func_type == 'string':
            return partial(TimeFormatFactory.datetime_to_string, time_format=time_format)
        elif func_type == 'timestamp':
            return TimeFormatFactory.datetime_to_timestamp
        else:
            return partial(TimeFormatFactory.datetime_to_string, time_format=time_format)