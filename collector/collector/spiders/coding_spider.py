# coding: utf-8

from __future__ import unicode_literals

import sys
sys.path.append('/Users/RaPoSpectre/PycharmProjects/RaPo3/')

import scrapy

# from scrapy.selector import HtmlXPathSelector
from collector.collector.items import CodingItem
from scrapy import Selector
from scrapy.http import Request

from core.utils import md5


class ProxySpider(scrapy.Spider):
    name = 'coding.net'
    host = 'https://mart.coding.net/'
    start_urls = ["https://mart.coding.net/projects?status=5"]

    def parse(self, response):
        for sel in response.xpath('//article[@id]'):
            item = CodingItem()
            item['amount'] = unicode(
                sel.xpath('div/div/div/div[@class="price"]/span/span/text()').extract()[
                    0]).strip().replace(",", "")
            item['title'] = '{0} | {1}'.format(unicode(
                sel.xpath('div/div/div/div[@class="name"]/a/text()').extract()[0]).strip(), item['amount'])
            item['role'] = unicode(
                sel.xpath('div/div/div/div[@class="coders"]/span/@title').extract()[0]).strip()
            item['type'] = unicode(
                sel.xpath('div/div/div/div[@class="type"]/div/span/text()').extract()[0]).strip()
            item['duration'] = unicode(
                sel.xpath('div/div/div/div[@class="type"]/label/span/b/text()').extract()[
                    0]).strip()
            url = unicode(
                sel.xpath('div/div/div/div[@class="name"]/a/@href').extract()[0]).strip()
            url = '{0}{1}'.format(self.host, url)
            item['url'] = url
            item['unique_id'] = md5(url)
            yield Request(url, meta={'item': item}, callback=self.parse_sub_page)

    def parse_sub_page(self, response):
        hxs = Selector(response)
        item = response.meta['item']
        item['extra'] = unicode(
            hxs.xpath('//*[@id="mart-reward-detail"]/div[1]/section[3]/div').extract()[0]).strip().lower()
        item['cache'] = response.body
        attachment = hxs.xpath('//*[@id="mart-reward-detail"]/div[1]/section[3]/div[5]/div/div/span[1]/input/@value')
        item['attachment'] = attachment.extract()[0].strip() if len(attachment) > 0 else ''
        return item
