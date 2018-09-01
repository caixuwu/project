# -*- coding: utf-8 -*-
import scrapy
from PIL import Image

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ['http://douban.com/']

    def parse(self, response):
        response.urljoin()
