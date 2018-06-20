# coding = utf-8
import importlib
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ip_proxy.ip_source import URL_LIST
from ip_proxy.config import SPIDER_SET
from ip_proxy.utils.log import log
from ip_proxy.connection.redis_connection import RedisConnection
import traceback

class Crawl(object):
    
    def __init__(self):
        r = RedisConnection(db = 1)
        self.conn = r.conn
        pass
    
    def start(self):
        try:
            settings = get_project_settings()
            process = CrawlerProcess(settings)
            if URL_LIST:
                for value in URL_LIST:
                    if not self.conn.sismember(SPIDER_SET,value['class']):
                        ip_module = importlib.import_module(value['module'])
                        ip_module_cls = getattr(ip_module, value['class'])
                        cls_obj = ip_module_cls()
                        process.crawl(cls_obj)
            process.start()
        except Exception as e:
            logger = log.getLogger('development')
            logger.error(traceback.format_exc())
            pass

crawler = Crawl()
        