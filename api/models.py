# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from core.models import BaseModel
from myguest.models import Guest


# Create your models here.


class Tag(BaseModel):
    title = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.title


class Classification(BaseModel):
    title = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.title


class Article(BaseModel):
    title = models.CharField(max_length=50)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='tag_arts')
    classification = models.ForeignKey(Classification, related_name='cl_arts')
    content = models.TextField()
    publish = models.BooleanField(default=False)
    slug = models.SlugField(max_length=50, default='')

    def __unicode__(self):
        return self.title


class Comment(BaseModel):
    content = models.TextField()
    author = models.ForeignKey(Guest, related_name='user_comments', null=True, blank=True, on_delete=models.SET_NULL)
    belong = models.ForeignKey(Article, related_name='art_comments')
    state = models.CharField(max_length=64, null=True, blank=True)
    review = models.BooleanField(default=False)

    def __unicode__(self):
        return '{0}-{1}'.format(self.author, self.create_time.strftime("%Y-%m-%d %H:%M:%S"))


class CommentReply(BaseModel):
    content = models.TextField()
    comment = models.ForeignKey(Comment, related_name='comment_replies')
    author = models.ForeignKey(Guest, related_name='user_comment_replies', null=True, blank=True,
                               on_delete=models.SET_NULL)
    to = models.ForeignKey(Guest, related_name='user_replied', null=True, blank=True, on_delete=models.SET_NULL)
    state = models.CharField(max_length=64, null=True, blank=True)
    review = models.BooleanField(default=False)

    def __unicode__(self):
        return '{0}->{1}'.format(self.author, self.to)


class Env(BaseModel):
    content = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.content


class Knowledge(BaseModel):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    publish = models.BooleanField(default=False)
    env = models.ManyToManyField(Env, related_name='knowledges')

    def __unicode__(self):
        return self.question


class Collection(BaseModel):
    priority_choice = [(3, '高优先'),
                       (2, '正常'),
                       (1, '低优先')]

    title = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    unique_id = models.CharField(max_length=64, unique=True)
    like = models.BooleanField(default=True)
    read = models.BooleanField(default=False)
    time = models.DateTimeField(default=None)
    priority = models.IntegerField(default=0, choices=priority_choice)
    cache = models.TextField(default='')
    attachment = models.CharField(max_length=128, default='')

    def __unicode__(self):
        return self.title
