# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from ip_proxy.database.mysql_helper import MysqlHelper
import time

class Ip66Pipeline(object):
    def process_item(self, item, spider):
        mysql = MysqlHelper()
        conn = mysql.conn
        cursor = conn.cursor()
        print(item)
        try:
            sql = "insert into `ip` (`ip`, `isp`, `country`, `region`, `city`, `area`, `create_time`) values ('%s', '%s', '%s', '%s', '%s', '%s', %f);" % (item['ip'], item['isp'], item['country'], item['region'], item['city'], item['area'], time.time())
            print(sql)
            res = cursor.execute(sql)
            print(res)
            conn.commit()
        except Exception as e:
            print(e)
            pass
        finally:
            conn.close()
