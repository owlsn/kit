# coding = utf-8
import os

ROOT = os.path.dirname(os.path.realpath(__file__))
LOG_PATH = ROOT + '/log/'
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
    'db' : 1,
    'password' : None,
}

