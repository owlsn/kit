from display.handlers.base import BaseHandler

class ExamplesInvoiceHandler(BaseHandler):
    def get(self):
        title = 'ExamplesInvoiceHandler'
        self.render('examples/invoice.html', title = title, **self.render_dict)