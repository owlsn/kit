# coding = utf-8

from ip_proxy.connection.mysql_connection import MysqlConnection
import time
import json
from ip_proxy.utils.log import log
import traceback
import copy

class CheckPipeline(object):

    def __init__(self):
        conn = MysqlConnection()
        self.dbpool = conn.dbpool
        pass

    def process_item(self, item, spider):
        # 异步插入数据库,出现过重复插入问题,主要问题可能是多线程抓取情况下item参数传递问题,item内存地址相同
        # logger = log.getLogger('debug')
        # logger.debug(json.dumps(item))
        asyncItem = copy.deepcopy(item)
        res = self.dbpool.runInteraction(self.do_update, asyncItem)
        res.addErrback(self.handle_error, asyncItem, spider)
        return item

    def handle_error(self, failure, item, spider):
        logger = log.getLogger('development')
        logger.error(str(failure))
        pass

    def do_update(self, cursor, item):
        logger = log.getLogger('development')
        update_sql, params = item.get_update_sql()
        try:
            cursor.execute(update_sql, params)
            logger.info('update_sql:{},params:{}'.format(update_sql, params))
        except Exception as e:
            logger.error('sql:' + update_sql)
            logger.error('params:' + json.dumps(params))
            logger.error(traceback.format_exc())
            pass