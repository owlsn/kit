# coding = utf-8
import os
import time

ROOT = os.path.abspath(os.path.dirname(__file__))

PUBLIC = ROOT + "/public/"

TEMPLATES = PUBLIC + "templates/"

STATIC = PUBLIC + "static/"

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

LOG_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/log/"
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
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
        "debug_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"DEBUG",
            "formatter":"simple",
            "filename": LOG_PATH + time.strftime("%Y-%m-%d", time.localtime())+".debug.log",
            "maxBytes":10485760,
            "backupCount":20,
            "encoding":"utf8"
        },
        "info_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"INFO",
            "formatter":"simple",
            "filename": LOG_PATH + time.strftime("%Y-%m-%d", time.localtime())+".info.log",
            "maxBytes":10485760,
            "backupCount":20,
            "encoding":"utf8"
        },
        "warn_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"WARNING",
            "formatter":"simple",
            "filename":LOG_PATH + time.strftime("%Y-%m-%d", time.localtime())+".warnings.log",
            "maxBytes":10485760,
            "backupCount":20,
            "encoding":"utf8"
        },
        "error_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"ERROR",
            "formatter":"simple",
            "filename":LOG_PATH + time.strftime("%Y-%m-%d", time.localtime())+".errors.log",
            "maxBytes":10485760,
            "backupCount":20,
            "encoding":"utf8"
        }
    },
    "loggers":{
        "debug":{
            "level":"DEBUG",
            "handlers":["debug_file_handler"],
            "propagate":"no"
        },
        "development":{
            "level":"INFO",
            "handlers":["info_file_handler"],
            "propagate":"no"
        },
        "production":{
            "level":"WARNING",
            "handlers":["warn_file_handler"],
            "propagate":"no"
        },
    }
}