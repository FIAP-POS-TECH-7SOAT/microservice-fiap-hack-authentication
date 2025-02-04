import smtplib

from src.shared.logger import LoggerFactory
from src.core.domain.application.services.Iemail_service import IMailSend
from src.adapters.drivens.infra.settings.env import ENV

class MailSend(IMailSend):
    
    def __init__(self):
        self.env = ENV()
        self.logger = LoggerFactory()
        self.smtp_server = self.env.EMAIL_HOST
        self.smtp_port = self.env.EMAIL_PORT
        self.smtp_user = self.env.EMAIL_USER
        self.smtp_password = self.env.EMAIL_PASSWORD
        
    def login_server(self):
        """Login in server"""
        try:
            self.logger.info("MailSend :: login_server :: Stablishing server")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            
            self.logger.info("MailSend :: login_server :: Starting server")
            server.starttls()
            
            self.logger.info(f"MailSend :: login_server :: Logging with user {self.smtp_user}")
            server.login(self.smtp_user, self.smtp_password)
            
            self.logger.info(f"MailSend :: login_server :: Server UP!")
            return server
        except Exception as ex:
            self.logger.error(f"MailSend :: mounting_server :: Error {ex}")
            
    def send_email(self, to_email:str, subject_mail:str, body:str):
        """Send email"""
        subject = subject_mail
        message = body
        try:
            self.logger.info("MailSend :: send_email :: Login on server")
            server = self.login_server()
            
            self.logger.info("MailSend :: send_email :: Sending email")
            server.sendmail(self.smtp_user, to_email, f"Subject: {subject}\n\n{message}")
            
            self.logger.info("MailSend :: send_email :: Shutingdown server")
            server.quit()
        except Exception as e:
            self.logger.error(f"MailSend :: send_mail :: Error sending email: {e}")