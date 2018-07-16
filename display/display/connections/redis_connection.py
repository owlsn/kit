# -*- coding: utf-8 -*-
import redis
from display.config import REDIS
import traceback
from display.utils.log import Log

# redis连接池
class RedisConnection(object):

    def __init__(self, host = None, port = None, db = None, password = None):
        try:
            self.config = REDIS
            self.pool = redis.ConnectionPool(
                host = host if host else self.config['host'], 
                port = port if port else self.config['port'],
                db = db if db else self.config['db'], 
                password = password if password else self.config['password']
                )
            self.conn = redis.Redis(connection_pool = self.pool)
            pass
        except Exception as e:
            logger = Log().getLogger('development')
            logger.error(traceback.format_exc())
            pass

redisDb1 = RedisConnection(db = 1)
redisDb0 = RedisConnection()
            

