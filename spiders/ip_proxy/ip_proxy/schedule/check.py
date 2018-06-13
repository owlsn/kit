# coding = utf-8
import os
import sys
p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(p)
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from ip_proxy.spiders.check import CheckSpider
from ip_proxy.utils.log import log
import traceback

if __name__ == '__main__':
    try:
        logger = log.getLogger('debug')
        logger.debug('test 123')
        check = CheckSpider()
        settings = get_project_settings()
        runner = CrawlerRunner(settings)
        runner.crawl(check)
    except Exception as e:
        logger = log.getLogger('debug')
        logger.debug(traceback.format_exc())
        pass
        