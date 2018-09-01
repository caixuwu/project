# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from company.settings import *

class CompanyPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient(DBHOST,DBPOST)
        self.db = self.conn.company
        self.my_table = self.db.info

    def process_item(self, item, spider):
        self.my_table.insert(dict(item))
        return item

    def closs_spider(self,spider):
        self.conn.close()