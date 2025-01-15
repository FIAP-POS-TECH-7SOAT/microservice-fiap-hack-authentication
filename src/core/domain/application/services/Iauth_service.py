from abc import ABC, abstractmethod
from src.core.domain.models.token_model import Token

class IAuthService(ABC):
    @abstractmethod
    def insert_refresh_token(self, token:Token):
        """Insert a new token into database."""
        pass
    
    @abstractmethod
    def get_refresh_token(self, user_email: str)->dict[str]|None:
        """Get a new refreshed token in database"""
        pass

    @abstractmethod
    def update_access_token_from_session_id(self, session_id: str, access_token: str):
        """Update access token based on session"""
        pass