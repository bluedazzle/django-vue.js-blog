# coding:utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import datetime
import copy
import json

import xmltodict
from django.db.models.fields.files import ImageFieldFile

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


def _include_check(include_attr, attr_dict):
    if not isinstance(attr_dict, dict):
        return attr_dict
    for itm in attr_dict.itervalues():
        if isinstance(itm, dict):
            _include_check(include_attr, itm)
        elif isinstance(itm, list):
            for sitm in itm:
                _include_check(include_attr, sitm)
    if include_attr:
        ex_attr_dict = copy.deepcopy(attr_dict)
        attr_dict.clear()
        for attr in include_attr:
            if attr in ex_attr_dict:
                attr_dict[attr] = ex_attr_dict.get(attr, None)
    return attr_dict


def _exclude_check(exclude_attr, attr_dict):
    if not isinstance(attr_dict, dict):
        return attr_dict
    for itm in attr_dict.itervalues():
        if isinstance(itm, dict):
            _exclude_check(exclude_attr, itm)
        elif isinstance(itm, list):
            for sitm in itm:
                _exclude_check(exclude_attr, sitm)
    if exclude_attr:
        for attr in exclude_attr:
            if attr in attr_dict:
                attr_dict.pop(attr)
    return attr_dict


def _get_attr(model_data, time_func, foreign, many):
    dic_list = model_data.__dict__
    attr_list = model_data._meta.get_all_field_names()
    for itm in attr_list:
        if not hasattr(model_data, itm):
            break
        attribute = getattr(model_data, itm)
        if isinstance(attribute, models.Model):
            if foreign:
                dic_list[itm] = _get_attr(attribute, time_func, foreign, many)
        elif isinstance(attribute, manager.Manager):
            if many and not str(itm).endswith('_art'):
                many_obj = attribute.all()
                many_list = []
                for mitm in many_obj:
                    many_item = _get_attr(mitm, time_func, foreign, many)
                    many_list.append(many_item)
                dic_list[itm] = many_list
        elif isinstance(attribute, (datetime.datetime, datetime.date, datetime.time)):
            dic_list[itm] = time_func(getattr(model_data, itm))
        elif isinstance(attribute, ImageFieldFile):
            dic_list[itm] = attribute.name
        elif isinstance(attribute, (list, QuerySet)):
            i_list = []
            for i in attribute:
                i_list.append(_get_attr(i, time_func, foreign, many))
            dic_list[itm] = i_list
        else:
            dic_list[itm] = getattr(model_data, itm)
    return_dict = {}
    for k, v in dic_list.iteritems():
        if not (unicode(k).startswith('_') and unicode(k).endswith('_cache')) and not (unicode(k) == '_state'):
            if isinstance(v, (list, QuerySet)):
                i_list = []
                for i in v:
                    i_list.append(_get_attr(i, time_func, False, False))
                return_dict[k] = i_list
            else:
                return_dict[k] = v
    return return_dict


def _data_convert(data, time_func, foreign, many, include_attr, exclude_attr):
    if isinstance(data, models.Model):
        attr_list = _get_attr(data, time_func, foreign, many)
        _include_check(include_attr, attr_list)
        _exclude_check(exclude_attr, attr_list)
        return attr_list
    elif isinstance(data, QuerySet):
        result = []
        for itm in data:
            attr_list = _get_attr(itm, time_func, foreign, many)
            _include_check(include_attr, attr_list)
            _exclude_check(exclude_attr, attr_list)
            result.append(copy.copy(attr_list))
        return result
    elif isinstance(data, (datetime.datetime, datetime.date)):
        return time_func(data)
    elif isinstance(data, (unicode, str, bool, float, int)):
        return data
    elif isinstance(data, dict):
        for k, v in data.iteritems():
            data[k] = _data_convert(v, time_func, foreign, many, include_attr, exclude_attr)
        return data
    elif isinstance(data, list):
        for i, itm in enumerate(data):
            data[i] = _data_convert(itm, time_func, foreign, many, include_attr, exclude_attr)
        return data
    else:
        return None


def _output_convert(output_type, data):
    output_switch = {'dict': data,
                     'raw': data,
                     'json': json.dumps(data, indent=4),
                     'xml': xmltodict.unparse({'root': data})}
    return output_switch.get(output_type, None)


def serializer(data, datetime_format='timestamp', output_type='raw', include_attr=None, exclude_attr=None,
               foreign=False, many=False, **kwargs):
    foreign = remove_check(**kwargs) or foreign
    time_func = TimeFormatFactory.get_time_func(datetime_format)
    result = _data_convert(data, time_func, foreign, many, include_attr, exclude_attr)
    return _output_convert(output_type, result)
