from abc import ABC, abstractmethod

from src.core.domain.application.ports.providers.dtos.token_response import TokenResponse
from src.core.domain.application.ports.providers.dtos.token_request_dto import TokenRequest
from src.core.domain.application.ports.providers.dtos.user_request_dto import UserRequest
class IAuthService(ABC):
    
    @abstractmethod
    def authenticate_user(self, user_request:UserRequest):
        """Authenticate user and generate a JWT signed with the shared private key."""
        pass
    
    @abstractmethod
    def verify_token(self, token:str)->TokenResponse:
        """Verify the JWT using the shared public key."""
        pass