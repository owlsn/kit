from display.handlers.base import BaseHandler

class MailboxHandler(BaseHandler):
    def get(self):
        title = 'MailboxHandler'
        self.render('mailbox/mailbox.html', title = title, **self.render_dict)