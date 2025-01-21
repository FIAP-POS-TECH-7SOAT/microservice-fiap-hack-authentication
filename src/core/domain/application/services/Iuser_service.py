
from abc import ABC, abstractmethod

from src.adapters.drivers.http.dtos.create_user_request_dto import CreateUserRequest



class IUserService(ABC):
    @abstractmethod
    def register_user(self, user_request:CreateUserRequest)->bool:
        """Register a new user with a hashed password."""
        pass
    
    @abstractmethod
    def delete_user(self, user_email: str)->str:
        """Delete user"""
        pass