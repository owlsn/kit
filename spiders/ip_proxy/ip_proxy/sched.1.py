# coding = utf-8
from apscheduler.schedulers.twisted  import TwistedScheduler
import time
import os
import sys
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)
from ip_proxy.utils.log import log
from ip_proxy.scheduler.crawl import crawler
from ip_proxy.scheduler.ip_queue import ip_queue
from twisted.internet import reactor

def job():
    try:
        crawler.start()
        pass
    except Exception as e:
        logger = log.getLogger('development')
        logger.error(traceback.format_exc())
    pass

def push_ip():
    try:
        ip_queue.do_select()
        pass
    except Exception as e:
        logger = log.getLogger('development')
        logger.error(traceback.format_exc())
    pass

# if __name__ == '__main__':
    # argv = sys.argv
    # if len(argv) < 2:
    #     exit()
    # if argv[1] == 'job':
    #     job()
    # elif argv[1] == 'push_ip':
    #     push_ip()

sched = TwistedScheduler()
logger = log.getLogger('development')
crawler.start(sched)
sched.add_job(job, 'cron', minute='*/1', id='job')
# sched.add_job(push_ip, 'cron', hour='*/1', id='push_ip')
  
logger.info('before the start funciton')
sched.start()  
try:
    reactor.run()
except (KeyboardInterrupt, SystemExit):
    pass
logger.info("let us figure out the situation")