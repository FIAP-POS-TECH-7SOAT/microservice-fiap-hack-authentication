from src.core.domain.application.services.auth_service import AuthService

class GetRefreshTokenUseCase:
    def __init__(self, auth_service:AuthService):
        self.auth_service = auth_service
        
    def execute(self, user_email:str):
        #Colocar um validador aqui
        return self.auth_service.get_refresh_token(user_email)