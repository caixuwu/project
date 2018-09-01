# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Field,Item


class JdlistItem(Item):
    # define the fields for your item here like:
    product = Field()
    url = Field()
    price = Field()
    all_comment = Field()
    best_comment = Field()
    agent_comment = Field()

