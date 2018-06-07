# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time

class Ip66Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = scrapy.Field()
    isp = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    create_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into `ip` (`ip`, `isp`, `country`, `region`, `city`, `area`, `create_time`) values (%s, %s, %s, %s, %s, %s, %s);"""
        params = (self['ip'], self['isp'], self['country'], self['region'], self['city'], self['area'], time.time())
        return insert_sql, params
            