# -*- coding: utf-8 -*-
from ip_proxy.config import MONGO

class MongoConnection():

    def __init__(self, host = None, port = None):
        self.config = MONGO
        h = host if host else self.config['host']
        p = port if port else self.config['port']
        s = 'mongodb://' + str(h) + ':' + str(p)
        
        pass