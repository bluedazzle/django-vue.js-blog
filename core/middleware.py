# coding: utf-8
from __future__ import unicode_literals
from raven.contrib.django.raven_compat.models import client


class ExceptCaptureMiddleware(object):
    def process_exception(self, request, exception):
        client.captureException()
        return None
