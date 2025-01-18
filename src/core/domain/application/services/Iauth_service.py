from abc import ABC, abstractmethod

from core.domain.application.ports.providers.dtos.user_request_dto import UserRequest
class IAuthService(ABC):
    
    @abstractmethod
    def authenticate_user(self, user_request:UserRequest):
        """Authenticate user and generate a JWT signed with the shared private key."""
        pass