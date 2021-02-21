# coding: utf-8

from __future__ import unicode_literals

import scrapy


class ProxySpider(scrapy.Spider):
    name = 'test'
    host = 'https://mart.coding.net/'
    start_urls = ["https://mart.coding.net/projects?status=5"]

    def parse(self, response):
        for sel in response.xpath('//article[@id]'):
            item = {}
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
            yield item
