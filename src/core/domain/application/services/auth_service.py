import base64
from datetime import datetime, timedelta

import bcrypt
from jose import jwt

from src.shared.logger import LoggerFactory
from src.adapters.drivers.http.dtos.token_request_dto import TokenRequest
from src.adapters.drivers.http.dtos.token_response import TokenResponse
from src.adapters.drivers.http.dtos.user_request_dto import UserRequest
from src.adapters.drivens.infra.repositories.user_repository import UserRepository
from src.adapters.drivens.infra.settings.env import ENV
from src.core.domain.application.services.Iauth_service import IAuthService
class AuthService(IAuthService):
    
    def __init__(self):
        self.logger = LoggerFactory()
        
        self.logger.info("AuthService :: Constructor :: Declaring UserRepository")
        self.user_repository = UserRepository()
        
        self.logger.info("AuthService :: Constructor :: Calling ENV")
        self.settings = ENV()
        
    def authenticate_user(self, user_credentials:UserRequest)->jwt.encode:
        """Authenticate user and generate a JWT signed with the shared private key."""
        try:
            self.logger.info(f"AuthService :: authenticate_user :: Get user from {user_credentials.user_email}")
            user = self.user_repository.get_user(user_credentials.user_email)

            if not user:
                self.logger.error(f"AuthService :: authenticate_user :: User does not exist")
                raise ValueError("User does not exist")
            
            if not user.email_verified:
                self.logger.error(f"AuthService :: authenticate_user :: User is not verified")
                raise ValueError(" User is not verified")
            
            hashed_password = user.password

            self.logger.info(f"AuthService :: authenticate_user :: Decode base64 Private Key")
            private_key = base64.b64decode(self.settings.PRIVATE_KEY).decode('utf-8')
            
            self.logger.info(f"AuthService :: authenticate_user :: Verifying if password match")    
            if not bcrypt.checkpw(user_credentials.password.encode(), str(hashed_password).encode()):
                self.logger.info(f"AuthService :: authenticate_user :: Invalid password")
                raise ValueError("Invalid password")
            
            try:
                self.logger.info(f"AuthService :: authenticate_user :: Generating token")
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
                self.logger.error(f"AuthService :: authenticate_user :: Error {ex}")
                raise ValueError(str(ex))
            
            return token
        
        except Exception as ex:
            self.logger.error(f"AuthService :: authenticate_user :: Error {ex}")
            raise ValueError(str(ex))
        
    
    def verify_token(self, token:TokenRequest)->TokenResponse:
        """Verify the JWT using the shared public key."""
        try:
            self.logger.info(f"AuthService :: verify_token :: Decoding base64 Public Key")
            public_key = base64.b64decode(self.settings.PUBLIC_KEY).decode('utf-8')

            self.logger.info(f"AuthService :: verify_token :: Building payload of user from token")
            payload = jwt.decode(token.token, public_key, algorithms=["RS256"])

            self.logger.info(f"AuthService :: verify_token :: Returning infos from user {payload['user_email']}")
            return payload
            
        except Exception as ex:
            self.logger.error(f"AuthService :: authenticate_user :: Error {ex}")
            raise ValueError(str(ex))
                
            