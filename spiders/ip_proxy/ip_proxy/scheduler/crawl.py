# coding = utf-8
import os
import importlib
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ip_proxy.config import SPIDER_SET
from ip_proxy.utils.log import log
from ip_proxy.connection.redis_connection import RedisConnection
import traceback
import yaml

class Crawl(object):
    
    def __init__(self):
        r = RedisConnection(db = 1)
        self.conn = r.conn
        pass
    
    def start(self):
        try:
            settings = get_project_settings()
            process = CrawlerProcess(settings)
            source = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/ip_source.yaml'
            with open(source, 'r') as f:
                data = yaml.load(f)
                if 'URL_LIST' in data and data['URL_LIST']:
                    for value in data['URL_LIST']:
                        if not self.conn.sismember(SPIDER_SET,value['class']):
                            ip_module = importlib.import_module(value['module'])
                            ip_module_cls = getattr(ip_module, value['class'])
                            cls_obj = ip_module_cls()
                            process.crawl(cls_obj)
                    process.start()
                    pass
                else:
                    raise Exception('yaml file is empty')
                    pass
        except Exception as e:
            logger = log.getLogger('development')
            logger.error(traceback.format_exc())
            pass

crawler = Crawl()
        