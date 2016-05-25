from django.shortcuts import render, render_to_response


# Create your views here.
from django.views.generic import TemplateView, DetailView

from api.models import Article


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
