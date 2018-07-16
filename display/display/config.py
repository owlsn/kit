# coding = utf-8
import os

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