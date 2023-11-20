from flask import Flask
from flask_mail import Message, Mail
from src.config.config import MAIL_CONFIG

app = Flask(__name__)
app.config.from_object(MAIL_CONFIG)

mail = Mail(app)


def send_mail(rcpt_email: str, title: str, sender_msg: str):
    with app.app_context():
        msg = Message(title,
                      sender='markpublicm@gmail.com',
                      recipients=[rcpt_email])
        msg.body = sender_msg
        mail.send(msg)
