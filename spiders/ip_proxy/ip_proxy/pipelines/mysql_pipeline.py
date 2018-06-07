# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from ip_proxy.database.mysql_helper import MysqlHelper
from ip_proxy.config import *
import time
import json
import traceback

class MysqlPipeline(object):
    def process_item(self, item, spider):
        mysql = MysqlHelper()
        conn = mysql.conn
        cursor = conn.cursor()
        try:
            sql = "insert into `ip` (`ip`, `isp`, `country`, `region`, `city`, `area`, `create_time`) values ('%s', '%s', '%s', '%s', '%s', '%s', %f);" % (item['ip'], item['isp'], item['country'], item['region'], item['city'], item['area'], time.time())
            res = cursor.execute(sql)
            print(sql)
            if res != 1:
                with open(LOG_PATH, 'a') as f:
                    f.writelines('item:' + json.dumps(dict(item)) + "\n")
                    f.write('sql:' + sql + "\n")
                f.close()
            else :
                conn.commit()
        except Exception as e:
            with open(LOG_PATH, 'a') as f:
                f.write('exception:' + traceback.format_exc() + "\n")
                f.write('item:' + json.dumps(dict(item)) + "\n")
                f.write('sql:' + sql + "\n")
            f.close()
        finally:
            conn.close()
        return item
