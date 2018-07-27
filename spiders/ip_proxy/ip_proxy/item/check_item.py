# coding = utf-8

import scrapy
import time
from ip_proxy.utils.log import Log
import traceback
from ip_proxy.config import QUEUE_NUM, CHECK_TIMES

class CheckItem(scrapy.Item):
    delay = scrapy.Field()
    level = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    scheme = scrapy.Field()
    times = scrapy.Field()
    key = scrapy.Field()

    def get_update_sql(self):
        try:
            if 'key' not in self.keys() or not self['key']:
                update_sql = None
                params = None
                return update_sql, params
            logger = Log().getLogger('development')
            if self['delay'] != -1:
                self['level'] = int(self['delay'] / 10000) + 1
                if self['level'] > (QUEUE_NUM - 1):
                    self['level'] = (QUEUE_NUM - 1)
                update_sql = """ update ip set delay = %s,level = %s,update_time = %s, times = 0 where id = %s """
                params = (self['delay'], self['level'], time.time(), self['key'])
            else:
                if 'times' in self.keys() and self['times'] is not None:
                    times = CHECK_TIMES if CHECK_TIMES else 3
                    if self['times'] > times:
                        update_sql = """ delete from ip where id = %s """
                        params = (self['key'])
                    else:
                        update_sql = """ update ip set delay = %s,level = %s,update_time = %s,times = times + 1 where id = %s """
                        params = (self['delay'], self['level'], time.time(), self['key'])
                        pass
                else:
                    update_sql = """ update ip set delay = %s,level = %s,update_time = %s, times = 1 where id = %s """
                    params = (self['delay'], self['level'], time.time(), self['key'])
                    pass
            # logger.info('sql:{},params:{}'.format(update_sql, params))
            return update_sql, params
            pass
        except Exception as e:
            logger = Log().getLogger('development')
            logger.error(traceback.format_exc())
            pass
            