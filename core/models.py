# coding: utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Secret(BaseModel):
    secret = models.CharField(max_length=64, unique=True)
    remark = models.CharField(max_length=20, default='web')

    def __unicode__(self):
        return self.remark
