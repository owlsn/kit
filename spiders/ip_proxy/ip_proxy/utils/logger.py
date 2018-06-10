# coding = utf-8

from scrapy import logging

class Logger(object):

    defalut_path = ''

    default_level = logging.INFO

    def __init__(self):
        if os.path.exists(default_path):
            logging.config.dictConfig(default_path)
        else:
            logging.basicConfig(level = default_level)
        pass
    