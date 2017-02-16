# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

class MongoPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(settings['MONGO']['default']['host'], settings['MONGO']['default']['port'])
        self.database = self.client[settings['MONGO']['default']['database']]
        self.collection = self.database[settings['MONGO']['default']['collection']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
