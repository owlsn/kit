# coding = utf-8

import scrapy
import time
from ip_proxy.utils.log import log
import traceback
from ip_proxy.config import QUEUE_NUM

class CheckItem(scrapy.Item):
    delay = scrapy.Field()
    level = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    scheme = scrapy.Field()

    def get_update_sql(self):
        try:
            if self['delay'] != -1:
                self['level'] = int(self['delay'] / 1000) + 1
                if self['level'] > (QUEUE_NUM - 1):
                    self['level'] = (QUEUE_NUM - 1)
            else:
                self['level'] = 0
            update_sql = """ update ip set delay = %s,level = %s,update_time = %s where ip = %s and port = %s and scheme = %s"""
            params = (self['delay'], self['level'], time.time(), self['ip'], self['port'], self['scheme'])
            return update_sql, params
            pass
        except Exception as e:
            logger = log.getLogger('development')
            logger.error(traceback.format_exc())
            pass
            