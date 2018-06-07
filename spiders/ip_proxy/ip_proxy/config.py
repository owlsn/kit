# coding = utf-8
import os

ROOT = os.path.dirname(os.path.realpath(__file__))
LOG_PATH = ROOT + '/file.log'
MYSQL = {
    'host' : '',
    'port' : 3306,
    'database' : '',
    'user' : '',
    'password' : '',
    'charset' : 'utf8'
}
REDIS = {
    'host' : '',
    'port' : 6379,
    'db' : 0,
    'passwd' : None,
}

