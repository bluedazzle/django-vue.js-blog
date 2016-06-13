# coding: utf-8

from __future__ import unicode_literals
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
import markdown

from api.models import Article


class ExtendedRSSFeed(Rss201rev2Feed):
    mime_type = 'application/xml'
    """
    Create a type of RSS feed that has content:encoded elements.
    """

    def root_attributes(self):
        attrs = super(ExtendedRSSFeed, self).root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement(u'content:encoded', 'utf-8')


class ArticleFeed(Feed):
    feed_type = ExtendedRSSFeed
    title = u"RaPoSpectre 的技术博客"
    link = ""
    description = "关注 RaPoSpectre 的最新动态"

    def items(self):
        return Article.objects.order_by('-create_time')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown.markdown(item.content)

    def item_link(self, item):
        return '/blog/{0}'.format(item.id)
