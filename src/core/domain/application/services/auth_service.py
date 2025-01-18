from datetime import datetime, timedelta

import bcrypt
import jwt

from src.core.domain.application.ports.providers.dtos.token_response import TokenResponse
from src.core.domain.application.ports.providers.dtos.token_request_dto import TokenRequest
from src.adapters.drivens.infra.repositories.keys_repository import KeysRepository
from src.adapters.drivens.infra.repositories.user_repository import UserRepository
from src.adapters.drivens.infra.settings.env import ENV
from src.core.domain.application.ports.providers.dtos.user_request_dto import UserRequest
from src.core.domain.application.services.Iauth_service import IAuthService
class AuthService(IAuthService):
    
    def __init__(self):
        self.user_repository = UserRepository()
        self.keys_repository = KeysRepository()
        self.settings = ENV()
        
    def authenticate_user(self, user_credentials:UserRequest)->jwt.JWT.encode:
        """Authenticate user and generate a JWT signed with the shared private key."""
        try:
            user = self.user_repository.get_user(user_credentials.user_email)
            
            if not user:
                raise ValueError("User does not exist")
            
            hashed_password = user.password
            if not bcrypt.checkpw(user_credentials.password.encode(), hashed_password):
                raise ValueError("Invalid credentials")
            
            key = self.keys_repository.get_key()
            
            token = jwt.JWT.encode(
                {
                    "sub": user.id,
                    "user_email": user.user_email,
                    "phone": user.phone,
                    "exp": datetime.astimezone() + timedelta(days=self.settings.EXP_DATE),
                    "iat": datetime.astimezone(),
                },
                key.private_key,
                algorithm="RS256",
            )
            
            return token
        
        except Exception as ex:
            raise ValueError(str(ex))
        
    
    def verify_token(self, token:TokenRequest)->TokenResponse:
        """Verify the JWT using the shared public key."""
        try:
            key = self.keys_repository.get_key()
            payload = jwt.JWT.decode(token, key.public_key, algorithms=["RS256"])
            return payload

        except jwt.JWT.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
            