# coding = utf-8

import scrapy
import time
from ip_proxy.utils.log import log
import traceback

class CheckItem(scrapy.Item):
    delay = scrapy.Field()
    level = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()

    def get_update_sql(self):
        try:
            if self['delay'] != -1:
                self['level'] = int(self['delay'] / 1000) + 1
            update_sql = """ update ip set delay = %s,level = %s,update_time = %s where ip = %s and port = %s"""
            params = (self['delay'], self['level'], time.time(), self['ip'], self['port'])
            return update_sql, params
            pass
        except Exception as e:
            logger = log.getLogger('development')
            logger.info(traceback.format_exc())
            pass
            