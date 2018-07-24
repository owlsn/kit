# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from ip_proxy.connection.redis_connection import redisDb1
from ip_proxy.config import SPIDER_SET
from ip_proxy.utils.log import Log
from ip_proxy.connection.mysql_connection import mysql

class BaseSpider(scrapy.Spider):

    def __init__(self):
        # redis连接,主要用于url判重
        self.conn = redisDb1.conn
        # 保存当前执行中的spider名称，以便在定时任务中判断
        self.spider_set = SPIDER_SET if SPIDER_SET else 'spider_set'
        logger = Log().getLogger('development')
        logger.info("{} init".format(self.__class__.__name__))
        pass

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)
        # 绑定singal，spider_closed和spider_opened
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider
        pass
    
    def spider_closed(self, spider, reason):
        # spider关闭去除集合中的对应标志数据
        cls_name = self.__class__.__name__
        self.conn.srem(self.spider_set, cls_name)
        # mysql.close()
        logger = Log().getLogger('development')
        logger.info("{} spider_closed".format(self))
        pass

    def spider_opened(self, spider):
        # spider开始在集合中加入对应标志数据
        cls_name = self.__class__.__name__
        self.conn.sadd(self.spider_set, cls_name)
        logger = Log().getLogger('development')
        logger.info("{} spider_opened".format(self))
        pass