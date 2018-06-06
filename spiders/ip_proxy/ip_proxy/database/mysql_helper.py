# coding = utf-8
import pymysql
from ip_proxy.config import MYSQL

class MysqlHelper(object):

    def __init__(self):
        self.config = MYSQL
        self.conn = pymysql.connect(self.config['host'], self.config['port'], self.config['user'], self.config['passwd'], self.config['database'], self.config['charset'])

    