from flask_mail import Message
from App import app, mail

def send_mail(rcpt_email: str, title: str, sender_msg: str):
    with app.app_context():
        message = Message(title, recipients=[rcpt_email])
        message.body =sender_msg
        mail.send(message)