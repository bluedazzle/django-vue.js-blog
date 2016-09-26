# coding: utf-8
from __future__ import unicode_literals

import random
import string

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView

from api.models import Article, Comment, CommentReply, Classification, Tag, Knowledge
from core.Mixin.CheckMixin import CheckTokenMixin, CheckAdminPermissionMixin, CheckSecurityMixin
from core.Mixin.JsonRequestMixin import JsonRequestMixin
from core.Mixin.StatusWrapMixin import *
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin, FormJsonResponseMixin
from myguest.models import Guest


class LoginView(CheckSecurityMixin, StatusWrapMixin, JsonRequestMixin, JsonResponseMixin, UpdateView):
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


class LogoutView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        request.session['token'] = ''
        return self.render_to_response(dict())


class ModifyArticleView(CheckSecurityMixin, CheckAdminPermissionMixin, StatusWrapMixin, JsonRequestMixin,
                        JsonResponseMixin, UpdateView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        aid = request.POST.get('id')
        content = request.POST.get('content')
        tags = request.POST.get('tags')
        slug = request.POST.get('slug', '')
        cid = request.POST.get('classification')
        publish = request.POST.get('publish', False)
        title = request.POST.get('title')
        slug = unicode(slug).replace(' ', '-').lower()
        if not unicode(aid).isdigit():
            aid = 0
        article = Article.objects.filter(id=aid)
        if article.exists():
            article = article[0]
            article.tags.clear()
        else:
            article = Article()
            article.publish = publish
        article.content = content
        classification = Classification.objects.get(id=cid)
        article.classification = classification
        article.title = title
        article.slug = slug
        article.save()
        for itm in tags:
            if itm and itm != '':
                tag = Tag.objects.filter(id=itm)
                if tag.exists():
                    article.tags.add(tag[0])
        article.save()
        return self.render_to_response(dict())


class ModifyKnowledgeView(CheckSecurityMixin, CheckAdminPermissionMixin, StatusWrapMixin, JsonRequestMixin,
                          JsonResponseMixin, UpdateView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        kid = request.POST.get('id')
        answer = request.POST.get('answer')
        publish = request.POST.get('publish', False)
        question = request.POST.get('question')
        if not unicode(kid).isdigit():
            kid = 0
        knowledge = Knowledge.objects.filter(id=kid)
        if knowledge.exists():
            knowledge = knowledge[0]
        else:
            knowledge = Knowledge()
            knowledge.publish = publish
        knowledge.answer = answer
        knowledge.question = question
        knowledge.save()
        return self.render_to_response(dict())


class AdminInfoView(CheckSecurityMixin, CheckAdminPermissionMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']
    include_attr = ['nick', 'avatar']

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        return self.render_to_response(self.admin)


class ArticlePublishView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']
    model = Article
    pk_url_kwarg = 'aid'

    def get_object(self, queryset=None):
        obj = super(ArticlePublishView, self).get_object(queryset)
        obj.publish = not obj.publish
        obj.save()
        return self.render_to_response(dict())


class KnowledgePublishView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']
    model = Knowledge
    pk_url_kwarg = 'kid'

    def get_object(self, queryset=None):
        obj = super(KnowledgePublishView, self).get_object(queryset)
        obj.publish = not obj.publish
        obj.save()
        return self.render_to_response(dict())


class CommentListView(CheckSecurityMixin, CheckAdminPermissionMixin, StatusWrapMixin, MultipleJsonResponseMixin,
                      ListView):
    http_method_names = ['get']
    model = Comment
    paginate_by = 2
    foreign = True
    include_attr = ['review', 'content', 'create_time', 'reply',
                    'id', 'author', 'avatar', 'nick', 'belong', 'title', 'to']

    def get_queryset(self):
        queryset = super(CommentListView, self).get_queryset()
        map(self.get_comment_reply, queryset)
        return queryset

    def get_comment_reply(self, comment):
        replies = comment.comment_replies.all()
        if replies.exists():
            setattr(comment, 'reply', True)
        else:
            setattr(comment, 'reply', False)
