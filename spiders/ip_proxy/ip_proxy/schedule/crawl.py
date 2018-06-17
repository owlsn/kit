# coding = utf-8
import os
import sys
p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(p)
import importlib
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ip_proxy.ip_source import URL_LIST
from ip_proxy.utils.log import log
import traceback

if __name__ == '__main__':
    try:
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        for value in URL_LIST:
            ip_module = importlib.import_module(value['module'])
            ip_module_cls = getattr(ip_module, value['class'])
            cls_obj = ip_module_cls()
            process.crawl(cls_obj)
        process.start()
    except Exception as e:
        logger = log.getLogger('debug')
        logger.debug(traceback.format_exc())
        pass
        