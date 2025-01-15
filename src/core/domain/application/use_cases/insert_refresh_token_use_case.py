from src.core.domain.application.services.auth_service import AuthService
from src.core.domain.models.token_model import Token

class InsertRefreshTokenUseCase:
    def __init__(self, auth_service:AuthService):
        self.auth_service = auth_service
        
    def execute(self, token:Token):
        #Colocar um validador aqui
        self.auth_service.insert_refresh_token(token)