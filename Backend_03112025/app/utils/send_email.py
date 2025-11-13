from flask_mail import Message
from ..extensions import mail

def send_otp_email(to_email, otp):
    """
    Sends OTP email using Flask-Mail.
    """
    msg = Message(
        subject="Your OTP Code",
        recipients=[to_email],
        body=f"Your OTP code for Todo App is: {otp}\nThis code will expire in 5 minutes."
    )
    mail.send(msg)
