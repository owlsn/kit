# coding = utf-8
from handlers import MainHandler
from handlers import HomeHandler
from handlers import IndexHandler

routers = [
    (r"/", MainHandler.MainHandler),
    (r"/index", IndexHandler.IndexHandler),
    (r"/home", HomeHandler.HomeHandler),
]