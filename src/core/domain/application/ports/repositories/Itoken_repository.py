from abc import ABC, abstractmethod
from src.core.domain.models.token_model import Token

class ITokenRepository(ABC):
    @abstractmethod
    def save_token(self, token:Token):
        """Insert a new token into database."""
        pass
    
    @abstractmethod
    def get_token_by_email(self, user_email:str)->dict[str]|None:
        """Get a new refreshed token in database"""
        pass

    @abstractmethod
    def get_token_by_session(self, session_id:str):
        """Update access token based on session"""
        pass
    
    @abstractmethod
    def delete_token(self, user_email:str):
        """Update access token based on session"""
        pass
    
    @abstractmethod
    def update_token(self, session_id: str, access_token: str):
        """Update access token based on session"""
        pass