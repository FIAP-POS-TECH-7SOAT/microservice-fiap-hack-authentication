import smtplib

from src.core.domain.application.services.Iemail_service import IMailSend
from src.adapters.drivens.infra.settings.env import ENV

class MailSend(IMailSend):
    
    def __init__(self):
        self.env = ENV()
        self.smtp_server = "smtp.example.com"
        self.smtp_port = 587
        self.smtp_user = "your-email@example.com"
        self.smtp_password = "your-email-password"
        
    def login_server(self):
        """Login in server"""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            return server
        except Exception as ex:
            print(f"MailSend :: mounting_server :: Error {ex}")
            
    def send_email(self, to_email:str, subject_mail:str, body:str):
        """Send email"""
        subject = subject_mail
        message = body

        try:
            server = self.login_server()
            server.sendmail(self.smtp_user, to_email, f"Subject: {subject}\n\n{message}")
            server.quit()
        except Exception as e:
            print(f"MailSend :: send_mail :: Error sending email: {e}")