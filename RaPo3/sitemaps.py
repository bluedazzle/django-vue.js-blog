# coding: utf-8

from __future__ import unicode_literals
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from api.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Article.objects.all()

    def lastmod(self, item):
        return item.create_time

    def location(self, item):
        return r'/blog/{0}'.format(item.id)


class StaticPageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return ['index', 'about', 'blogs']

    def location(self, item):
        return reverse(item)




