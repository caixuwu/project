# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisSpider
from JDlist import items

class JdspiderSpider(CrawlSpider):
    name = 'jdspider'
    allowed_domains = ['jd.com']
    # todo:
    redis_key = 'jdqueue:start_urls'

    rules = (
        Rule(LinkExtractor(allow='https:'+r'//item.jd.com/[0-9]*.html'), callback='parse_item', follow=True),
    )

    # def parse_start_url(self, response):
    def start_requests(self):
        urls = ['https://list.jd.com/list.html?cat=10,672&page=' + str(i) for i in range(1, 1019)]
        for url in urls:
            yield self.make_requests_from_url(url)

    def parse_item(self, response):
        i = items.JdlistItem()
        i['product'] = response.xpath('//div[@class="sku-name"]/text()').get().strip()
        i['url'] = response.url

        # i['price'] = response.xpath().get()
        # i['all_comment'] = response.xpath().get()
        # i['best_comment'] = response.xpath().get()
        # i['agent_comment'] = response.xpath().get()

        return i
