from src.core.domain.models.user_model import User

from abc import ABC, abstractmethod

class IUserRepository(ABC):
    @abstractmethod
    def save_user(self, user:User):
        pass
    
    @abstractmethod
    def get_user(self, user_email:str)->User:
        pass
    
    @abstractmethod
    def delete_user(self, user_email:str):
        pass
    
    @abstractmethod
    def update_password(self, user_email: str, password:str):
        pass