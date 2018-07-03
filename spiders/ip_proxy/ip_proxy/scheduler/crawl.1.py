# coding = utf-8
import os
import importlib
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from ip_proxy.utils.log import log
import traceback
import yaml
import time

class Crawl(object):
    
    def start(self, sched):
        try:
            logger = log.getLogger('development')
            timeArray = time.localtime(time.time())
            date_time = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
            logger.info('crawl start at:{}'.format(date_time))
            
            settings = get_project_settings()
            runner = CrawlerRunner(settings)
            source = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/ip_source.yaml'
            with open(source, 'r') as f:
                data = yaml.load(f)
                if 'URL_LIST' in data and data['URL_LIST']:
                    for value in data['URL_LIST']:
                        ip_module = importlib.import_module(value['module'])
                        ip_module_cls = getattr(ip_module, value['class'])
                        cls_obj = ip_module_cls()
                        sched.add_job(runner.crawl, value['type'], hour='*/1', id=value['id'],
                        args=[cls_obj], max_instances = value['max_instances'], coalesce = value['coalesce'])
                    d = runner.join()
                    d.addBoth(lambda _: reactor.stop())
                    # reactor.run()
                    pass
                else:
                    raise Exception('yaml file is empty')
                    pass
        except Exception as e:
            logger = log.getLogger('development')
            logger.error(traceback.format_exc())
            pass

crawler = Crawl()
        