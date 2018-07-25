# coding = utf-8
# import os
# import sys
# p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(p)
from ip_proxy.connection.redis_connection import redisDb1
from ip_proxy.connection.mysql_connection import mysqlSyn
from ip_proxy.config import QUEUE_NUM
import traceback
from ip_proxy.utils.log import Log
import time

class IpQueue(object):

    def __init__(self):
        self.redis = redisDb1.conn
        self.mysql = mysqlSyn.conn
        pass

    def getQueue(self, level):
        key = 'ip_queue_' + str(level)
        return key

    def do_select(self):
        try:
            logger = Log().getLogger('development')
            timeArray = time.localtime(time.time())
            date_time = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
            logger.info('ip_queue start at:{}'.format(date_time))
            
            for i in range(QUEUE_NUM):
                length = self.redis.llen(self.getQueue(i))
                print('length:{},i:{}'.format(length, i))
                if length < 10000:
                    start = 0
                    limit = 2500
                    sql = """select ip, port, scheme, level, flag, times from `ip` where level = %s order by update_time asc limit %s,%s """
                    while True:
                        params = (i, start * limit, limit)
                        cursor = self.mysql.cursor()
                        cursor.execute(sql, params)
                        res = cursor.fetchall()
                        if not res:
                            break
                        for value in res:
                            data = {'ip' : value[0], 'port' : value[1], 'scheme' : value[2], 'level' : value[3], 'flag':value[4], 'times' : value[5]}
                            if data['level'] is not None:
                                self.redis.rpush(self.getQueue(data['level']), data)
                            else:
                                self.redis.rpush(self.getQueue(0), data)
                        start = start + 1
            pass
        except Exception as e:
            mysqlSyn.connect()
            logger = Log().getLogger('development')
            logger.error(traceback.format_exc())
            pass

# if __name__ == '__main__':
#     ip_queue = IpQueue()
#     ip_queue.do_select()