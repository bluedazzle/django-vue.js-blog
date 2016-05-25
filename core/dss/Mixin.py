# coding: utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import json
from django.core.paginator import EmptyPage

from .Serializer import serializer
from .TimeFormatFactory import TimeFormatFactory

try:
    from django.http import HttpResponse
except ImportError:
    raise RuntimeError('django is required in django simple serializer')


class JsonResponseMixin(object):
    datetime_type = 'string'
    foreign = False
    many = False
    include_attr = None
    exclude_attr = None

    def time_format(self, time_obj):
        time_func = TimeFormatFactory.get_time_func(self.datetime_type)
        return time_func(time_obj)

    def context_serialize(self, context):
        if hasattr(context, 'get'):
            if context.get('object', None):
                context.pop('object')
        return serializer(data=context,
                          datetime_format=self.datetime_type,
                          output_type='raw',
                          foreign=self.foreign,
                          many=self.many,
                          include_attr=self.include_attr,
                          exclude_attr=self.exclude_attr)

    def json_serializer(self, context):
        return json.dumps(context, indent=4)

    def render_to_response(self, context, **response_kwargs):
        context_dict = self.context_serialize(context)
        json_context = self.json_serializer(context_dict)
        return HttpResponse(json_context, content_type='application/json', **response_kwargs)


class FormJsonResponseMixin(JsonResponseMixin):
    def context_serialize(self, context):
        form_list = []
        form = context.get('form', None)
        if form:
            for itm in form.fields:
                f_dict = {'field': unicode(itm)}
                form_list.append(f_dict)
        context_dict = super(FormJsonResponseMixin, self).context_serialize(context)
        context_dict['form'] = form_list
        return context_dict


class MultipleJsonResponseMixin(JsonResponseMixin):
    def context_serialize(self, context):
        if hasattr(context, 'get'):
            if context.get('object_list', None):
                context.pop('object_list')
        page_dict = {}
        is_paginated = context.get('is_paginated', None)
        if is_paginated:
            page_obj = context['page_obj']
            page_dict['current'] = page_obj.number
            page_dict['total'] = page_obj.paginator.num_pages
            try:
                previous_page = page_obj.previous_page_number()
            except EmptyPage:
                previous_page = None
            try:
                next_page = page_obj.next_page_number()
            except EmptyPage:
                next_page = None
            page_dict['previous'] = previous_page
            page_dict['next'] = next_page
            page_dict['page_range'] = [{'page': i} for i in page_obj.paginator.page_range]
        context_dict = super(MultipleJsonResponseMixin, self).context_serialize(context)
        context_dict['page_obj'] = page_dict
        return context_dict
