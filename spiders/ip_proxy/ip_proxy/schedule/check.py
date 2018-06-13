# coding = utf-8
import os
import sys
p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(p)
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ip_proxy.spiders.check import CheckSpider
from ip_proxy.utils.log import log
import traceback

if __name__ == '__main__':
    try:
        check = CheckSpider()
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        process.crawl(check)
        process.start()
    except Exception as e:
        logger = log.getLogger('debug')
        logger.debug(traceback.format_exc())
        pass
        