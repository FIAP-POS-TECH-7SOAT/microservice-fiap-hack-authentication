from abc import ABC, abstractmethod

class IMailSend(ABC):
    @abstractmethod
    def login_server(self):
        """Login in server"""
        pass
            
    @abstractmethod 
    def send_email(self, to_email:str, subject_mail:str, body:str):
        """Send email"""
        pass