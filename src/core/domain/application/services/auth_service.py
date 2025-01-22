import base64
from datetime import datetime, timedelta

import bcrypt
from jose import jwt

from src.adapters.drivers.http.dtos.token_request_dto import TokenRequest
from src.adapters.drivers.http.dtos.token_response import TokenResponse
from src.adapters.drivers.http.dtos.user_request_dto import UserRequest
from src.adapters.drivens.infra.repositories.user_repository import UserRepository
from src.adapters.drivens.infra.settings.env import ENV
from src.core.domain.application.services.Iauth_service import IAuthService
class AuthService(IAuthService):
    
    def __init__(self):
        self.user_repository = UserRepository()
        self.settings = ENV()
        
    def authenticate_user(self, user_credentials:UserRequest)->jwt.encode:
        """Authenticate user and generate a JWT signed with the shared private key."""
        try:
            user = self.user_repository.get_user(user_credentials.user_email)

            if not user:
                raise ValueError("User does not exist")
            
            hashed_password = user.password

            private_key = base64.b64decode(self.settings.PRIVATE_KEY).decode('utf-8')
                
            if not bcrypt.checkpw(user_credentials.password.encode(), str(hashed_password).encode()):
                raise ValueError("Invalid credentials")
            
            try:
                token = jwt.encode(
                    {
                        "sub": user.id,
                        "user_email": user.user_email,
                        "phone": user.phone,
                        "exp": datetime.now() + timedelta(days=int(self.settings.EXP_DATE)),
                        "iat": datetime.now(),
                    },
                    private_key,
                    algorithm="RS256",
                )
            except Exception as ex:
                raise ValueError(str(ex))
            
            return token
        
        except Exception as ex:
            raise ValueError(str(ex))
        
    
    def verify_token(self, token:TokenRequest)->TokenResponse:
        """Verify the JWT using the shared public key."""
        try:
            public_key = base64.b64decode(self.settings.PUBLIC_KEY).decode('utf-8')

            payload = jwt.decode(token.token, public_key, algorithms=["RS256"])
        
            return payload
            
        except Exception as ex:
            raise ValueError(str(ex))
                
            