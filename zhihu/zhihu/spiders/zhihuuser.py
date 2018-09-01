# -*- coding: utf-8 -*-
import scrapy


class ZhihuuserSpider(scrapy.Spider):
    name = 'zhihuuser'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    def start_requests(self):
        url = 'https://www.zhihu.com/api/v4/members/spto/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=1780&limit=20'
        yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        print(response.text)
