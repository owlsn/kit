# coding = utf-8
import os

ROOT = os.path.dirname(os.path.realpath(__file__))
LOG_PATH = ROOT + '/log/'
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
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

