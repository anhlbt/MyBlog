from threading import Thread
from flask import current_app
from flask_mail import Message, Mail
# from app.extensions import mail
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import pdb

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate


# If using STARTTLS with MAIL_USE_TLS = True, then use MAIL_PORT = 587.
# If using SSL/TLS directly with MAIL_USE_SSL = True, then use MAIL_PORT = 465.
# Enable either STARTTLS or SSL/TLS, not both.



# def send_async_email(app, msg, mail):
#     with app.app_context():
#         mail.send(msg)


# def send_email(subject, sender, recipients, text_body, html_body, attachments=None, sync=False):
#     mail=Mail()
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     # pdb.set_trace()
#     mail.init_app(current_app._get_current_object())
#     print(current_app._get_current_object())
#     if attachments:
#         for attachment in attachments:
#             msg.attach(*attachment)
#     if sync:
#         mail.connect()
#         mail.send(msg)
#     else:
#         Thread(target=send_async_email, args=(current_app._get_current_object(), msg, mail)).start()



def send_async_email(app, msg, mail):
    with app.app_context():
        mail.sendmail(msg['From'],msg['To'],msg.as_string())


def send_email(subject, sender, recipients, text_body, html_body,attachments=None, sync=False):
    app = current_app._get_current_object()
    # pdb.set_trace()
    # msg = MIMEText(text_body, 'plain', 'utf-8')
    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text_body))
    mail = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'], timeout=20)
    mail.starttls()
    mail.login(app.config['MAIL_SENDER'], app.config['MAIL_PASSWORD'])
    if attachments:
        # pdb.set_trace()
        # ('posts.json', 'application/json', '{\n    "posts": [\n        {\n            "body": "test content ...",\n            "timestamp": "2020-06-24T08:26:49.050451Z"\n        }\n    ]\n}')
        for f in attachments or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(fil.read(), Name=basename(f))
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)        
            
        # for attachment in attachments:
        #     msg.attach(*attachment)
    if sync:
        try:
            mail.sendmail(msg['From'], msg['To'], msg.as_string())
            assert('send mail successed....')
            # mail.close()
        finally:
            mail.quit()
    else:
        Thread(target=send_async_email, args=(app, msg, mail)).start()
