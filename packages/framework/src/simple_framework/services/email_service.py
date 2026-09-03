from ast import expr_context
import smtplib
from email.message import EmailMessage

from config import email_config

class EmailService:

    @staticmethod
    def send(
        receiver_email: str,
        subject: str,
        message: str
    ) -> bool:
        mail = EmailMessage()
        mail["From"] = email_config.EMAIL
        mail["To"] = receiver_email
        mail["Subject"] = subject
        mail.set_content(message)
        
        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(email_config.EMAIL, email_config.EMAIL_PASSWORD)
                server.send_message(mail)
                return True
        except:
            return False