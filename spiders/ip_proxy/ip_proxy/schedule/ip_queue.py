# coding = utf-8
import os
import sys
p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(p)
from ip_proxy.connection.redis_connection import RedisConnection
from ip_proxy.connection.mysql_connection import MysqlConnection
from ip_proxy.config import QUEUE_NUM
import traceback
from ip_proxy.utils.log import log

class IpQueue(object):

    def __init__(self):
        r = RedisConnection(db = 1)
        self.redis = r.conn
        m = MysqlConnection(type = 'syn')
        self.mysql = m.conn
        pass

    def getQueue(self, level):
        key = 'ip_queue_' + str(level)
        return key

    def do_select(self):
        try:
            sql = """select ip, port, scheme, level, flag from `ip` order by update_time asc"""
            cursor = self.mysql.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            for value in res:
                data = {'ip' : value[0], 'port' : value[1], 'scheme' : value[2], 'level' : value[3], 'flag':value[4]}
                if data['level'] is not None:
                    self.redis.rpush(self.getQueue(data['level']), data)
                else:
                    self.redis.rpush(self.getQueue(0), data)
            pass
        except Exception as e:
            logger = log.getLogger('development')
            logger.info(traceback.format_exc())
            pass

if __name__ == '__main__':
    try:
        ip_queue = IpQueue()
        ip_queue.do_select()
        pass
    except Exception as e:
        logger = log.getLogger('development')
        logger.info(traceback.format_exc())
        pass