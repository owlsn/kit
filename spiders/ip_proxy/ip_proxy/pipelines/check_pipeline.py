# coding = utf-8

from ip_proxy.connection.mysql_connection import mysqlAsyn
from ip_proxy.connection.redis_connection import redisDb1
from ip_proxy.config import QUEUE_KEY
import time
import json
from ip_proxy.utils.log import Log
import traceback
import copy

class CheckPipeline(object):

    def __init__(self):
        self.conn = mysqlAsyn.dbpool
        self.redis = redisDb1.conn
        pass

    def process_item(self, item, spider):
        # 异步插入数据库,出现过重复插入问题,主要问题可能是多线程抓取情况下item参数传递问题,item内存地址相同
        # logger = Log().getLogger('debug')
        # logger.debug(json.dumps(item))
        asyncItem = copy.deepcopy(item)
        res = self.conn.runInteraction(self.do_update, asyncItem)
        res.addErrback(self.handle_error, asyncItem, spider)
        return item

    def handle_error(self, failure, item, spider):
        logger = Log().getLogger('development')
        logger.error(str(failure))
        pass

    def do_update(self, cursor, item):
        logger = Log().getLogger('development')
        update_sql, params = item.get_update_sql()
        try:
            if update_sql is not None:
                cursor.execute(update_sql, params)
                data = {'key': item['key'], 'ip': item['ip'], 'port': item['port'], 'scheme': item['scheme'], 'level': item['level'], 'flag': 1, 'times': 1}
                logger.info('update_sql:{},params:{},data:{}'.format(update_sql, params, data))
                self.redis.rpush(QUEUE_KEY + str(item['level']), data)
        except Exception as e:
            logger.error('sql:{}'.format(update_sql))
            logger.error('params:{}'.format(params))
            logger.error(traceback.format_exc())
            pass