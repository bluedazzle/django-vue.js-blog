# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from core.models import BaseModel


# Create your models here.

class Guest(BaseModel):
    avatar = models.CharField(max_length=256, default='/s/image/avatar.png')
    nick = models.CharField(max_length=128)
    email = models.CharField(max_length=256, unique=True)
    forbid = models.BooleanField(default=False)
    token = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return '{0}-{1}'.format(self.nick, self.email)
