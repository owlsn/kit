from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    def initialize(self):
        show_header = 1
        show_aside = 1
        show_footer = 1
        self.render_dict = {'show_header' : show_header, 'show_aside' : show_aside, 'show_footer' : show_footer, 'uri' : self.request.uri}
