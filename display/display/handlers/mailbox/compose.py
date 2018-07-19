from display.handlers.base import BaseHandler

class MailboxComposeHandler(BaseHandler):
    def get(self):
        title = 'MailboxComposeHandler'
        self.render('mailbox/compose.html', title = title, **self.render_dict)