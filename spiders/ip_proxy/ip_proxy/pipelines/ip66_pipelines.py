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
        li = item['ip_list']
        try:
            for index, value in enumerate(li):
                sql = "insert into `ip` (`ip`, `isp`, `country`, `region`, `city`, `area`, `create_time`, ) values \
                (%s, %s, %s, %s, %s, %s, %f)" % (value['ip'], value['isp'], value['country'], value['region'], value['city'], value['area'], time.time())
                print(sql)
                cursor.execute(sql)
                conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()
