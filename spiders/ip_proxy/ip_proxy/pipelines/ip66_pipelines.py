# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from ip_proxy.item.ip66_item import Ip66Item

class Ip66Pipeline(object):
    def process_item(self, Ip66Item, spider):
        print(Ip66Item)
        pass
        return item
