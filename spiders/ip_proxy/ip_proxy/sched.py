# coding = utf-8
from apscheduler.schedulers.twisted  import TwistedScheduler
import time
import os
import sys
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)
from ip_proxy.utils.log import Log
from ip_proxy.scheduler.crawl import crawler
from ip_proxy.scheduler.ip_queue import IpQueue
from twisted.internet import reactor

def push_ip():
    try:
        ip_queue = IpQueue()
        ip_queue.do_select()
        pass
    except Exception as e:
        logger = Log().getLogger('development')
        logger.error(traceback.format_exc())
    pass

sched = TwistedScheduler()
logger = Log().getLogger('development')
crawler.start(sched)
sched.add_job(push_ip, 'cron', hour='*/2', id='push_ip')
sched.start()
logger.info('sched start')
reactor.run()
logger.info('sched end')