# coding: utf-8
from __future__ import unicode_literals

import random
import string

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView

from api.models import Article, Comment, CommentReply, Classification, Tag
from core.Mixin.CheckMixin import CheckTokenMixin, CheckAdminPermissionMixin
from core.Mixin.JsonRequestMixin import JsonRequestMixin
from core.Mixin.StatusWrapMixin import *
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin, FormJsonResponseMixin
from myguest.models import Guest


class LoginView(StatusWrapMixin, JsonRequestMixin, JsonResponseMixin, UpdateView):
    http_method_names = ['post']
    count = 64

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'rapospectre@gmail.com' and password:
            guest = Guest.objects.get(email=username)
            if guest.check_password(password):
                token = self.create_token()
                guest.token = token
                guest.save()
                request.session['token'] = token
                return self.render_to_response(dict())
            self.message = '密码错误'
            self.status_code = ERROR_PASSWORD
            return self.render_to_response(dict())
        self.message = '账号不存在'
        self.status_code = ERROR_ACCOUNT_NO_EXIST
        return self.render_to_response(dict())

    def create_token(self):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          self.count)).replace(" ", "")


class LogoutView(StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        request.session['token'] = ''
        return self.render_to_response(dict())


class ModifyArticleView(CheckAdminPermissionMixin, StatusWrapMixin, JsonRequestMixin, JsonResponseMixin, UpdateView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        aid = request.POST.get('aid')
        content = request.POST.get('content')
        tags = request.POST.get('tags')
        cid = request.POST.get('classification')
        publish = request.POST.get('publish', False)
        title = request.POST.get('title')
        article = Article.objects.filter(id=aid)
        if article.exists():
            article = article[0]
            article.tags.clear()
        else:
            article = Article()
        article.content = content
        classification = Classification.objects.get(id=cid)
        article.classification = classification
        article.title = title
        article.save()
        for itm in tags:
            tag = Tag.objects.filter(id=itm)
            if tag.exists():
                article.tags.add(tag[0])
        article.publish = publish
        article.save()
        return self.render_to_response(dict())


class AdminInfoView(CheckAdminPermissionMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']
    include_attr = ['nick', 'avatar']

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        return self.render_to_response(self.admin)


class ArticlePublishView(CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']
    model = Article
    pk_url_kwarg = 'aid'

    def get_object(self, queryset=None):
        obj = super(ArticlePublishView, self).get_object(queryset)
        obj.publish = not obj.publish
        obj.save()
        return self.render_to_response(dict())
