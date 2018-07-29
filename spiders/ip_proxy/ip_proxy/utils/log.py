# coding = utf-8

import logging
from logging import config
from ip_proxy.config import LOG_CONFIG
from ip_proxy.connection.mongo_connection import MongoConnection
import json

class Log(object):
    
    def __init__(self):
        self.logging = logging
        if LOG_CONFIG:
            self.config = LOG_CONFIG
            self.logging.config.dictConfig(LOG_CONFIG)
        else:
            self.logging.basicConfig(level = logging.INFO)

    def getLogger(self, logger):
        return self.logging.getLogger(logger)

class MongoLog(logging.Handler):

    def __init__(self):
        conn = MongoConnection()
        
        # self.config_engine = create_engine(configdb_str)
        # self.ConfigSession = sessionmaker(bind = self.config_engine)
        # self.config_session = self.ConfigSession()
        # metadata = MetaData(self.config_engine)
        # log_table = Table(table_name, metadata,
        #     Column('id', Integer, primary_key = True),
        #     Column('create_time', DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00.000'")),
        #     Column('level_name', String(10)),
        #     Column('message', String(255)),
        #     Column('splilt_type', String(10)),
        #     Column('split_base', String(10)),
        #     Column('exc_info', String(255)),
        #     Column('exc_text', String(255)),
        #     Column('file_name', String(100)),
        #     Column('line_no', Integer),
        #     Column('func_name', String(255)),
        #     Column('stack_info', String(255)))
        # metadata.create_all(self.config_engine)
        # self.LogModel = getModel(table_name, self.config_engine)
        logging.Handler.__init__(self)
        pass

    def emit(self, record):
        level = record.levelname
        message = record.message
        exc_info = record.exc_info
        exc_text = record.exc_text
        file_name = record.filename
        line_no = record.lineno
        func_name = record.funcName
        stack_info = record.stack_info
        document = {'level': level, 'message': message, 'exc_info':exc_info , 'exc_text': exc_text, 'file_name': file_name,
            'line_no': line_no, 'func_name': func_name, 'stack_info': stack_info}
        self.do_insert()

        # with open('test.log', 'a') as f:
        #     f.write(json.dumps({'level': level, 'message': message, 'exc_info':exc_info , 'exc_text': exc_text, 'file_name': file_name,
        #     'line_no':line_no, 'func_name':func_name, 'stack_info':stack_info}) + "\n")
        pass

    async def do_insert(self):
        document = {'key': 'value'}