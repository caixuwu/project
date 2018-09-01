# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item,Field

class Company(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    com_name = Field()
    share_profit = Field()
    profit = Field()
    grow_rise_profit = Field()
    product_profit = Field()
    grow_rise_prodeuct_profit = Field()
    gross_revenue = Field()
    grow_rise_gross_revenue = Field()
    per_share = Field()
    share_earn_rise = Field()
    per_share_dilute = Field()
    debt_ratio = Field()
    accumulat_fund = Field()
    undivided_profit = Field()
    cash_flow = Field()
    product_earn = Field()
    product_turnover = Field()
    sale_profit = Field()