# coding: utf-8
from __future__ import unicode_literals

import json
import random
import string

import datetime
import markdown

import time

from django.core.serializers import serialize
from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect
from django.utils.timezone import get_current_timezone
from django.views.generic import ListView, DetailView, CreateView, TemplateView, DeleteView

from RaPo3.settings import HOST
from api.models import Article, Comment, CommentReply, Classification, Tag, Knowledge, Collection
from core.Mixin.CheckMixin import CheckTokenMixin, CheckSecurityMixin
from core.Mixin.JsonRequestMixin import JsonRequestMixin
from core.Mixin.StatusWrapMixin import *
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin, FormJsonResponseMixin

# Create your views here.
from core.dss.Serializer import serializer
from core.github import get_github_auth, get_access_token, get_user_info
from core.qn import generate_upload_token
from core.utils import save_image, upload_picture, send_html_mail, string_to_datetime
from myguest.models import Guest
from django.core.mail import send_mail

import hashlib


class ArticleDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Article
    pk_url_kwarg = 'aid'
    foreign = True

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object(queryset)
        obj.views += 1
        obj.save()
        setattr(obj, 'tag_list', obj.tags.all())
        return obj


class ArticleListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Article
    foreign = True
    exclude_attr = ['content', 'modify_time']
    paginate_by = 2

    def get_queryset(self):
        all = self.request.GET.get('all')
        cid = self.request.GET.get('cid')
        tag = self.request.GET.get('tag')
        query = self.request.GET.get('query')
        admin = self.request.GET.get('admin')
        queryset = super(ArticleListView, self).get_queryset().order_by('-create_time')
        if not admin:
            queryset = queryset.filter(publish=True)
        if all:
            self.paginate_by = 0
        elif query:
            self.paginate_by = 5
            if query == 'popular':
                queryset = queryset.order_by("-views")
        else:
            if cid:
                classification = Classification.objects.filter(id=cid)
                if classification.exists():
                    queryset = queryset.filter(classification=classification[0])
                else:
                    queryset = queryset.filter(classification__id=-1)
            if tag:
                tag = Tag.objects.filter(id=tag)
                if tag.exists():
                    queryset = queryset.filter(tags=tag[0])
                else:
                    queryset = queryset.filter(tags__id=-1)
            map(self.get_summary, queryset)
            map(self.get_comment_number, queryset)
            map(self.get_tag, queryset)
        return queryset

    def get_summary(self, article):
        setattr(article, 'summary', markdown.markdown(article.content[:400]))

    def get_comment_number(self, article):
        comment_list = Comment.objects.filter(belong=article, review=True)
        count = comment_list.count()
        for comment in comment_list:
            count += comment.comment_replies.all().filter(review=True).count()
        setattr(article, 'comment_number', count)

    def get_tag(self, article):
        tag_list = article.tags.all()
        setattr(article, 'tag_list', tag_list)


class CommentListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    http_method_names = ['get']
    model = Comment
    foreign = True
    exclude_attr = ['belong', 'token', 'email', 'modify_time']

    def get_queryset(self):
        queryset = super(CommentListView, self).get_queryset()
        article = Article.objects.get(id=self.kwargs.get('aid'))
        queryset = queryset.filter(belong=article, review=True).order_by("-create_time")
        map(self.get_reply, queryset)
        return queryset

    def get_reply(self, comment):
        reply_list = CommentReply.objects.filter(comment=comment, review=True)
        if reply_list.exists():
            for reply in reply_list:
                setattr(reply, 'reply', serializer(reply.to, include_attr=['nick', 'id', 'avatar']))
                setattr(reply, 'create_by', serializer(reply.author, include_attr=['nick', 'id', 'avatar']))
            setattr(comment, 'replies', reply_list)
        else:
            setattr(comment, 'replies', [])


class CommentView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonRequestMixin, JsonResponseMixin,
                  CreateView):
    http_method_names = ['post']
    model = Comment
    count = 32

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        aid = kwargs.get('aid')
        cid = request.POST.get('cid')
        tid = request.POST.get('tid')
        reply = unicode(request.POST.get('reply', '-1'))
        if reply == '1':
            comments = Comment.objects.filter(id=cid)
            if not comments.exists():
                self.message = '回复评论不存在'
                self.status_code = INFO_NO_EXIST
                return self.render_to_response(dict())
            toer = Guest.objects.get(id=tid)
            comment = CommentReply(comment=comments[0],
                                   to=toer)
        else:
            article = Article.objects.filter(id=aid)
            if not article.exists():
                self.message = '评论文章不存在'
                self.status_code = INFO_NO_EXIST
                return self.render_to_response(dict())
            comment = Comment()
            comment.belong = article[0]

        if content:
            comment.content = content
        else:
            self.message = '请输入评论内容'
            self.status_code = ERROR_DATA
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            state = self.generate_state()
            comment.state = state
            comment.save()
            url = get_github_auth(state)
            return self.render_to_response({'url': url})
        else:
            comment.author = self.user
            comment.review = True
            comment.save()
            send_mail('新评论', '你有一条新评论, 登陆查看 www.rapospectre.com ', 'bluedazzle@163.com',
                      ['rapospectre@gmail.com'],
                      fail_silently=True)
            if isinstance(comment, CommentReply):
                send_html_mail('评论回复', comment.to, comment.comment.belong, [comment.to.email])
            return self.render_to_response(dict())

    def generate_state(self):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          self.count)).replace(" ", "")


class LoginCallbackView(TemplateView):
    http_method_names = ['get']
    template_name = 'blog/detail.html'
    count = 64

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        state = request.GET.get('state')
        if code and state:
            access_token = get_access_token(code, state)
            gid, email, nick, avatar = get_user_info(access_token)
            guest = Guest.objects.filter(uid=gid)
            token = self.create_token()
            if guest.exists():
                guest = guest[0]
                guest.token = token
                guest.save()
            else:
                # status, avatar_path = save_image(avatar, '{0}{1}.png'.format(nick, unicode(time.time()).split('.')[0]))
                guest = Guest(email=email, nick=nick, token=token, uid=gid)
                guest.set_password('123456q_+|')
                # if status:
                guest.avatar = avatar
                guest.save()
            comment = Comment.objects.filter(state=state)
            aid = 0
            if not comment.exists():
                comment = CommentReply.objects.filter(state=state)
            else:
                aid = comment[0].belong.id
                send_mail('新评论', '你有一条新评论, 登陆查看 www.rapospectre.com', 'bluedazzle@163.com',
                          ['rapospectre@gmail.com'], fail_silently=True)
            if comment.exists():
                comment = comment[0]
                comment.author = guest
                comment.review = True
                comment.save()
                if aid == 0:
                    aid = comment.comment.belong.id
                    send_html_mail('评论回复', comment.to, comment.comment.belong, [comment.to.email])
            request.session['token'] = token
            return HttpResponseRedirect('/blog/{0}'.format(aid))

    def create_token(self):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          self.count)).replace(" ", "")


class UserInfoView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']
    include_attr = ['nick', 'id', 'avatar']

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            self.message = 'sign 验证失败'
            self.status_code = ERROR_PERMISSION_DENIED
            return self.render_to_response(dict())
        if self.wrap_check_token_result():
            return self.render_to_response(self.user)
        return self.render_to_response({'avatar': '/s/image/avatar.png'})


class ClassificationView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    http_method_names = ['get']
    include_attr = ['title', 'id']
    model = Classification


class TagView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    http_method_names = ['get']
    include_attr = ['title', 'id']
    model = Tag


class UploadView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, CreateView):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        token = generate_upload_token()
        return HttpResponse(json.dumps({'uptoken': token}), content_type='application/json')

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('editormd-image-file')
        path, sp = upload_picture(image_file)
        data = json.dumps({'url': '{0}{1}'.format(HOST, path),
                           'success': 1,
                           'message': '成功'})
        return HttpResponse(data, content_type='application/json')


class KnowListView(CheckSecurityMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    http_method_names = ['get']
    model = Knowledge
    paginate_by = 20
    many = True
    exclude_attr = ['modify_time']

    def get_queryset(self):
        query = self.request.GET.get('query', None)
        admin = self.request.GET.get('admin', None)
        queryset = super(KnowListView, self).get_queryset()
        if not admin:
            queryset = queryset.filter(publish=True)
        if query:
            queryset = queryset.filter(Q(question__icontains=query) | Q(answer__icontains=query))
        queryset = queryset.order_by("-create_time")
        return queryset


class KnowDetailView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['get']
    pk_url_kwarg = 'kid'
    model = Knowledge


class CollectionsListView(CheckSecurityMixin, StatusWrapMixin, JsonRequestMixin, MultipleJsonResponseMixin, ListView):
    http_method_names = ['get', 'post']
    exclude_attr = ['cache']
    model = Collection
    paginate_by = 20
    ordering = ('-priority', 'like', '-read', '-create_time')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        url = request.POST.get('url')
        news_time = request.POST.get('time')
        if not news_time:
            news_time = datetime.datetime.now(tz=get_current_timezone())
        else:
            news_time = string_to_datetime(news_time)
        md5 = hashlib.md5(title).hexdigest()
        news = Collection.objects.filter(unique_id=md5)
        if not (title and url):
            self.status_code = ERROR_DATA
            self.message = '信息缺失'
            return self.render_to_response({})
        if news.exists():
            self.status_code = INFO_EXISTED
            self.message = '消息已存在'
            return self.render_to_response({})
        News(title=title, url=url, unique_id=md5, time=news_time).save()
        return self.render_to_response({})
