# coding = utf-8
import os

ROOT = os.path.dirname(os.path.realpath(__file__))

MYSQL = {
    'host' : '119.27.170.185',
    'port' : 3306,
    'database' : 'ip_proxy',
    'user' : 'root',
    'passwd' : '123456',
    'charset' : 'utf8'
}

LOG_PATH = ROOT + '/file.log'