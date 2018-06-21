# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time
import socket
import struct
from ip_proxy.utils.log import log
import traceback

class IpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    isp = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    scheme = scrapy.Field()
    source = scrapy.Field()

    def get_insert_sql(self):
        if 'scheme' not in self.keys() or not self['scheme']:
            self['scheme'] = 'http'
        if 'source' not in self.keys() or not self['source']:
            self['source'] = 'unknown'
        if 'ip' in self.keys() and self['ip'] and 'port' in self.keys() and self['port']:
            insert_sql = """insert into `ip` (`ip`, `port`, `create_time`, `scheme`, `delay`, `level`, `source`) values (%s, %s, %s, %s, %s, %s, %s);"""
            try:
                params = (struct.unpack('!I', socket.inet_aton(self['ip']))[0], self['port'], time.time(), self['scheme'], -1, 0, self['source'])
                pass
            except Exception as e:
                logger = log.getLogger('development')
                logger.error('ip is invalid:{}'.format(self['ip']))
                logger.error(traceback.format_exc)
                pass
            return insert_sql, params
        else:
            return None
            