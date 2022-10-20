import os
from update_summarizer import mail
from flask_mail import Message

def send_mail(to: str, subject: str, body: str):
    msg=Message("Password Reset Request", 
                sender=os.getenv("MAIL_USERNAME"), 
                recipients=[to])
    
    msg.subject = subject
    msg.html = body
    mail.send(msg)