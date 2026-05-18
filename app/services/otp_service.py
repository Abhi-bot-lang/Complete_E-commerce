import smtplib
from email.message import EmailMessage
import os

def send_otp_email(receiver, code):
    msg = EmailMessage()
    msg.set_content(f"Your code is {code}")
    msg['Subject'] = "OTP Code"
    msg['From'] = os.getenv("EMAIL_SENDER")
    msg['To'] = receiver

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)