# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time
import socket
import struct
from ip_proxy.utils.ip_address import IpAddress

class Ip66Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    isp = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()

    def get_insert_sql(self):
        ip = self['ip']
        if ip:
            r = IpAddress.info(ip)
            if r != None and r['code'] == 0:
                data = r['data']
                self['isp'] = data['isp']
                self['country'] =data['country']
                self['city'] = data['city']
                self['region'] = data['region']
                self['area'] = data['area']
        insert_sql = """insert into `ip` (`ip`, `port`, `isp`, `country`, `region`, `city`, `area`, `create_time`) values (%s, %s, %s, %s, %s, %s, %s, %s);"""
        params = (struct.unpack('!I', socket.inet_aton(self['ip']))[0], self['port'], self['isp'], self['country'], self['region'], self['city'], self['area'], time.time())
        return insert_sql, params
            