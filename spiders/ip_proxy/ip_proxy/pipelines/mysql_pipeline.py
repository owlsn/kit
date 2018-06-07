# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from ip_proxy.config import *
import pymysql
import time
import json
import traceback

class MysqlPipeline(object):

    def __init__(self):
        self.config = MYSQL
        self.conn = pymysql.connect(host = self.config['host'], 
        user = self.config['user'], password = self.config['passwd'], 
        database = self.config['database'], port = self.config['port'], 
        charset = self.config['charset'])
        pass


    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        try:
            sql = "insert into `ip` (`ip`, `isp`, `country`, `region`, `city`, `area`, `create_time`) values ('%s', '%s', '%s', '%s', '%s', '%s', %f);" % (item['ip'], item['isp'], item['country'], item['region'], item['city'], item['area'], time.time())
            res = cursor.execute(sql)
            #print(sql)
            if res != 1:
                raise Exception('insert failed!');
            else :
                self.conn.commit()
        except Exception as e:
            with open(LOG_PATH, 'a') as f:
                f.write('exception:' + traceback.format_exc() + "\n")
                f.write('item:' + json.dumps(dict(item)) + "\n")
                f.write('sql:' + sql + "\n")
            f.close()
        return item
