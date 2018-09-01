# -*- coding: utf-8 -*-
import json

import scrapy
from company.items import Company
import scrapy.selector
from scrapy.spider import CrawlSpider
import re
class FinancialSpider(scrapy.Spider):
    name = 'finance'
    allowed_domains = ['10jqka.com.cn']

    def start_requests(self):
        for i in range(1,67):
            if i <10:
                rep = scrapy.Request(url='http://q.10jqka.com.cn/thshy/detail/code/88110%d/'%i,callback=self.urlitem)
                yield rep
            else:
                rep = scrapy.Request(url = 'http://q.10jqka.com.cn/thshy/detail/code/8811%d/' % i, callback=self.urlitem)
                yield rep

    def urlitem(self, response):
        urls = response.xpath('//*[@id="maincont"]/table/tbody/tr/td[2]/a/@href').extract()
        for i in urls:
            url = i.replace('stockpage','basic')[0:-1]+'/finance.html'
            req = scrapy.Request(url=url,callback=self.parse)
            yield req



    def parse(self, response):
        i = Company()
        data = response.xpath('//p[@id="main"]/text()').get()
        Date = json.loads(data)['report']
        i['com_name'] = response.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/h1/a/@title').get()
        i['share_profit'] = Date[1]
        i['profit'] = Date[2]
        i['grow_rise_profit'] = Date[3]
        i['product_profit'] = Date[4]
        i['grow_rise_prodeuct_profit'] = Date[5]
        i['gross_revenue'] = Date[6]
        i['grow_rise_gross_revenue'] = Date[7]
        i['per_share'] = Date[8]
        i['share_earn_rise'] = Date[9]
        i['per_share_dilute'] = Date[10]
        i['debt_ratio'] = Date[11]
        i['accumulat_fund'] = Date[12]
        i['undivided_profit'] = Date[13]
        i['cash_flow'] = Date[14]
        i['product_earn'] = Date[15]
        i['product_turnover'] = Date[16]
        i['sale_profit'] = Date[17]
        return i


