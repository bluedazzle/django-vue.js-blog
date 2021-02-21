# coding: utf-8

import os
import sys

from collector.collector.settings import BASE_DIR

sys.path.append(BASE_DIR)

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from spiders.coding_spider import CodingProjectSpider


class CodingSpiderAgent(object):
    def __init__(self):
        self.crawler = None

    def crawl(self):
        os.environ['SCRAPY_PROJECT'] = '{0}/{1}'.format(BASE_DIR, 'collector')
        runner = CrawlerRunner({'LOG_LEVEL': 'WARNING',
                                'LOG_FORMATTER': 'collector.collector.utils.PoliteLogFormatter',
                                'ITEM_PIPELINES': {
                                    'collector.collector.pipelines.CodingDuplicatesPipeline': 1,
                                    'collector.collector.pipelines.CodingPriorityPipeline': 2
                                }})
        # runner = CrawlerRunner()
        d = runner.crawl(CodingProjectSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()


crawler = CodingSpiderAgent()


def crawl():
    crawler.crawl()
