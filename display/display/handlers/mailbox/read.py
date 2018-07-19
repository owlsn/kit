from display.handlers.base import BaseHandler

class MailboxReadHandler(BaseHandler):
    def get(self):
        title = 'MailboxReadHandler'
        self.render('mailbox/read-mail.html', title = title, **self.render_dict)