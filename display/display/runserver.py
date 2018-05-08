import tornado.ioloop
import tornado.web
import routers
import os
import config

def make_app():
    return tornado.web.Application(routers.routers)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)

    #print("root_path:" + root_path);
    #print("public_path:" + public_path);
    #print("template_path:" + template_path);
    #print("static_path:" + static_path);
    
    tornado.ioloop.IOLoop.current().start()