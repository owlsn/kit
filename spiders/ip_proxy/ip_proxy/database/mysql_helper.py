# coding = utf-8
import pymysql
from ip_proxy.config import MYSQL

class MysqlHelper(object):

    def __init__(self):
        self.config = MYSQL
        self.conn = pymysql.connect(host = self.config['host'], 
        user = self.config['user'], password = self.config['passwd'], 
        database = self.config['database'], port = self.config['port'], 
        charset = self.config['charset'])