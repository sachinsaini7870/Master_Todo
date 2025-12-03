from flask_mail import Message
from ..extensions import mail

def send_otp_email(to_email, otp, link=""):
    """
    Sends OTP email using Flask-Mail.
    """
    
    msg = Message(
        subject="Your OTP Code",
        recipients=[to_email],
        body=f"Your OTP code for Todo App is: {otp}\nThis code will expire in 5 minutes.\n {link}"
    )
    mail.send(msg)

def send_link_email(to_email, restLink):
    """
    Sends OTP email using Flask-Mail.
    """
    
    msg = Message(
        subject="Todo App Reset Link",
        recipients=[to_email],
        body=f"Your rest password link for Todo App is: \nLink : {restLink}\nThis link will expire in 5 minutes.\n"
    )
    mail.send(msg)
