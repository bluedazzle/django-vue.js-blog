# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import datetime
import requests
from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone

from api.models import Comment, CommentReply


class Command(BaseCommand):
    def handle(self, *args, **options):
        comments = Comment.objects.all()
        for comment in comments:
            comment.review = True
            comment.save()

        replies = CommentReply.objects.al()
        for reply in replies:
            reply.review = True
            reply.save()