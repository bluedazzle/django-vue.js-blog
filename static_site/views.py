# coding: utf-8
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, HttpResponseRedirect

# Create your views here.
from django.views.generic import TemplateView, DetailView

from api.models import Article
from core.Mixin.CheckMixin import CheckAdminPagePermissionMixin, CheckAdminPermissionMixin


class BlogView(DetailView):
    http_method_names = ['get']
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'aid'
    model = Article


class BlogListView(TemplateView):
    http_method_names = ['get']
    template_name = 'blog/list.html'


class IndexView(TemplateView):
    http_method_names = ['get']
    template_name = 'blog/index.html'


class AboutView(TemplateView):
    http_method_names = ['get']
    template_name = 'blog/about.html'


class AdminLoginView(CheckAdminPermissionMixin, TemplateView):
    http_method_names = ['get']
    template_name = 'admin/admin_login.html'

    def get(self, request, *args, **kwargs):
        if self.wrap_check_token_result():
            return HttpResponseRedirect('/admin/index')
        return super(AdminLoginView, self).get(request, *args, **kwargs)


class AdminIndexView(CheckAdminPagePermissionMixin, TemplateView):
    http_method_names = ['get']
    template_name = 'admin/admin_index.html'


class AdminArticleListView(CheckAdminPagePermissionMixin, TemplateView):
    http_method_names = ['get']
    template_name = 'admin/article.html'


class AdminCommentListView(TemplateView):
    http_method_names = ['get']
    template_name = 'admin/comment.html'


class AdminModifyArticleView(CheckAdminPagePermissionMixin, DetailView):
    http_method_names = ['get']
    template_name = 'admin/modify_article.html'
    model = Article
    pk_url_kwarg = 'aid'

    def get_object(self, queryset=None):
        if not self.kwargs.get(self.pk_url_kwarg, None):
            return None
        return super(AdminModifyArticleView, self).get_object(queryset)
