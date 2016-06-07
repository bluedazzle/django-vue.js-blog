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
    tags = models.ManyToManyField(Tag, blank=True, related_name='tag_arts', null=True)
    classification = models.ForeignKey(Classification, related_name='cl_arts')
    content = models.TextField()
    publish = models.BooleanField(default=False)

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
