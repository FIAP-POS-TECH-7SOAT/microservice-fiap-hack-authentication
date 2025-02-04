
from abc import ABC, abstractmethod

from src.core.domain.models.user_model import User
from src.adapters.drivers.http.dtos.create_user_request_dto import CreateUserRequest


class IUserService(ABC):
    @abstractmethod
    def get_user_by_email(self, user_email: str)->User:
        """Get user by email"""
    
    @abstractmethod
    def update_password(self, user_email: str, new_password: str)->bool:
        """Update password based on token and update it with a new password"""
        pass
    
    @abstractmethod
    def register_user(self, user_request:CreateUserRequest)->bool:
        """Register a new user with a hashed password."""
        pass
    
    @abstractmethod
    def delete_user(self, user_email: str)->str:
        """Delete user"""
        pass