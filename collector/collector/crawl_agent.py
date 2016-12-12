# coding: utf-8

import os
import sys

from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from spiders.coding_spider import ProxySpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


class CodingSpiderAgent(object):
    def __init__(self):
        self.crawler = None

    def crawl(self):
        sys.path.append('/Users/RaPoSpectre/PycharmProjects/RaPo3/')
        os.environ['SCRAPY_PROJECT'] = '/Users/RaPoSpectre/PycharmProjects/RaPo3/collector'
        runner = CrawlerRunner({'LOG_LEVEL': 'ERROR',
                                'ITEM_PIPELINES': {
                                    'collector.collector.pipelines.CodingDuplicatesPipeline': 1,
                                    'collector.collector.pipelines.CodingPriorityPipeline': 2
                                }})
        # runner = CrawlerRunner()
        d = runner.crawl(ProxySpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

        # def crawl(self):
        #     sys.path.append('/Users/RaPoSpectre/PycharmProjects/RaPo3/')
        #     os.environ['SCRAPY_PROJECT'] = '/Users/RaPoSpectre/PycharmProjects/RaPo3/collector'
        #     process = CrawlerProcess({'LOG_LEVEL': 'ERROR',
        #                               'ITEM_PIPELINES': {
        #                                   'collector.collector.pipelines.CodingDuplicatesPipeline': 1,
        #                                   'collector.collector.pipelines.CodingPriorityPipeline': 2
        #                               }})
        #     process.crawl(ProxySpider)
        #     process.start()


crawler = CodingSpiderAgent()


def crawl():
    crawler.crawl()


# crawl()
