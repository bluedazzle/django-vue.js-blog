from __future__ import unicode_literals

from django.db import models

# Create your models here.
from core.models import BaseModel


class Domain(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    due_date = models.DateTimeField(null=True, blank=True)
    register = models.CharField(max_length=256, default='')
    reg_date = models.DateTimeField(null=True, blank=True)
    reg_email = models.CharField(max_length=100, default='')
    available = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class WeUser(BaseModel):
    openid = models.CharField(max_length=128, unique=True)
    session = models.CharField(max_length=256, unique=True)
    weapp_session = models.CharField(max_length=256, unique=True)
    nick = models.CharField(max_length=50, default='')
    avatar = models.CharField(max_length=128, default='')
    domain_list = models.ManyToManyField(Domain, related_name='domain_keepers')

    def __unicode__(self):
        return self.openid



