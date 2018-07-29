# coding = utf-8
import os
import time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MYSQL = {
    'host' : '127.0.0.1',
    'port' : 3306,
    'database' : 'ip_proxy',
    'user' : 'root',
    'password' : '123456',
    'charset' : 'utf8'
}
REDIS = {
    'host' : '127.0.0.1',
    'port' : 6379,
    'db' : 0,
    'password' : '',
}
MONGO = {
    'host': '127.0.0.1',
    'port' : 27017
}
LOG_PATH =  ROOT + "/log/"
IMAGE_PATH= ROOT + "/images/"
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
if not os.path.exists(IMAGE_PATH):
    os.mkdir(IMAGE_PATH)
LOG_CONFIG = {
    "version":1,
    "disable_existing_loggers":False,
    "formatters":{
        "simple":{
            "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers":{
        "console":{
            "class":"logging.StreamHandler",
            "level":"DEBUG",
            "formatter":"simple",
            "stream":"ext://sys.stdout"
        },
        "file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"INFO",
            "formatter":"simple",
            "filename": LOG_PATH + time.strftime("%Y-%m-%d", time.localtime())+".info.log",
            "maxBytes":10485760,
            "backupCount":20,
            "encoding":"utf8"
        },
        "mongo_handler":{
            "class": "ip_proxy.utils.log.MongoLog",
            "level": "DEBUG",
            "formatter": "simple"
        }
    },
    "loggers":{
        "development":{
            "level":"DEBUG",
            "handlers":["file_handler"],
            "propagate":"no"
        }
    }
}
# ip队列配置
QUEUE_NUM = 6
QUEUE_KEY = 'ip_queue_'

# spider 进程在redis中的set集合名
SPIDER_SET = 'spider_set'

# check_url
CHECK_URL = 'https://www.baidu.com/'

# CHECK_TIMES
CHECK_TIMES = 3