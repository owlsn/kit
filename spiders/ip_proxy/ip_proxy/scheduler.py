# coding = utf-8
import schedule
import time
import os
import sys
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)
from ip_proxy.scheduler.crawl import crawler
from ip_proxy.scheduler.ip_queue import ip_queue
 
def job():
    try:
        ip_queue.do_select()
        crawler.start()
        pass
    except Exception as e:
        logger = log.getLogger('development')
        logger.error(traceback.format_exc())
    pass

# schedule.every(6).hours.do(job)
 
# while True:
#     schedule.run_pending()
#     time.sleep(60 * 60)

if __name__ == '__main__':
    job()