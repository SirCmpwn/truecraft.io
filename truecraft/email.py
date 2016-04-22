import smtplib
import pystache
import os
import html.parser
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
from flask import url_for

from truecraft.database import db
from truecraft.objects import User
from truecraft.config import _cfg, _cfgi

def send_confirmation(user):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/confirm-account") as f:
        message = MIMEText(html.parser.HTMLParser().unescape(\
            pystache.render(f.read(), { 'user': user, "domain": _cfg("domain"), 'confirmation': user.confirmation })))
    message['X-MC-Important'] = "true"
    message['X-MC-PreserveRecipients'] = "false"
    message['Subject'] = "Confirm your TrueCraft account"
    message['From'] = _cfg("smtp-user")
    message['To'] = user.email
    smtp.sendmail(_cfg("smtp-user"), [ user.email ], message.as_string())
    smtp.quit()

def send_reset(user):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/reset") as f:
        message = MIMEText(html.parser.HTMLParser().unescape(\
            pystache.render(f.read(), {
                'user': user,
                "domain": _cfg("domain"),
                "protocol": _cfg("protocol"),
                'confirmation': user.passwordReset
            })))
    message['X-MC-Important'] = "true"
    message['X-MC-PreserveRecipients'] = "false"
    message['Subject'] = "Reset your TrueCraft password"
    message['From'] = _cfg("smtp-user")
    message['To'] = user.email
    smtp.sendmail(_cfg("smtp-user"), [ user.email ], message.as_string())
    smtp.quit()
