# coding = utf-8
# import os
# import sys
# p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(p)
# from twisted.internet import reactor

from ip_proxy.connection.redis_connection import redisDb1
from ip_proxy.connection.mysql_connection import mysqlAsyn
from ip_proxy.config import QUEUE_NUM
import traceback
from ip_proxy.utils.log import Log
import time

class IpQueue(object):

    def __init__(self):
        self.redis = redisDb1.conn
        self.dbpool = mysqlAsyn.dbpool
        self.logger = Log().getLogger('development')
        pass

    def getQueue(self, level):
        key = 'ip_queue_' + str(level)
        return key

    def handle_error(self, failure):
        self.logger.info(str(failure))
        pass

    def start(self):
        timeArray = time.localtime(time.time())
        date_time = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
        self.logger.info('ip_queue start at:{}'.format(date_time))
        for i in range(QUEUE_NUM):
            try:
                length = self.redis.llen(self.getQueue(i))
                if length < 10000:
                    index = i
                    res = self.dbpool.runInteraction(self.do_select, index)
                    res.addErrback(self.handle_error)
                pass
            except Exception as e:
                self.logger.info(traceback.format_exc())
                pass
        pass

    def do_select(self, cursor, i):
        try:
            length = self.redis.llen(self.getQueue(i))
            if length < 10000:
                start = 0
                limit = 2500
                sql = """select id, ip, port, scheme, level, flag, times from `ip` where level = %s order by update_time asc limit %s,%s """
                while True:
                    params = (i, start * limit, limit)
                    cursor.execute(sql, params)
                    res = cursor.fetchall()
                    if not len(res):
                        break
                    for value in res:
                        data = {'key': value['id'], 'ip': value['ip'], 'port': value['port'], 'scheme': value['scheme'], 'level': value['level'], 'flag': value['flag'], 'times': value['times']}
                        if data['level'] is not None:
                            self.redis.rpush(self.getQueue(data['level']), data)
                        else:
                            self.redis.rpush(self.getQueue(0), data)
                    start = start + 1
        except Exception as e:
            self.logger.error(traceback.format_exc())
            pass

# if __name__ == '__main__':
#     ip_queue = IpQueue()
#     ip_queue.start()
#     try:
#         reactor.run()
#         pass
#     except Exception as e:
#         print('stop')
#         pass