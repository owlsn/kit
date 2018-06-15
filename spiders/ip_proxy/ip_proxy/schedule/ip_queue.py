# coding = utf-8
from ip_proxy.connection.redis_connection import RedisConnection
from ip_proxy.connection.mysql_connection import MysqlConnection
from ip_proxy.config import QUEUE_NUM

class IpQueue(object):

    def __init__(self):
        r = RedisConnection(db = 1)
        self.conn = r.conn
        conn = MysqlConnection()
        self.dbpool = conn.dbpool
        pass

    def getQueue(self, level):
        key = 'ip_queue_' + level
        return key

    def get_ip(self):
        self.dbpool.runInteraction(self.do_select)
        res.addErrback(self.handle_error)
        pass

    def do_select(self, cursor):
        sql = """select ip, port, scheme, level from `ip` order by update_time asc"""
        res = cursor.execute(sql)
        for value in res:
            if value['level'] is not None:
                self.conn.rpush(self.getQueue(value['level']), value)
            else:
                self.conn.rpush(self.getQueue(0), value)
        pass

    def handle_error(self, failure, item, spider):
        logger = log.getLogger('development')
        logger.error(str(failure))
        pass