from src.core.domain.application.services.auth_service import AuthService

class UpdateAccessTokenUseCase:
    def __init__(self, auth_service:AuthService):
        self.auth_service = auth_service
        
    def execute(self, session_id:str, access_token:str):
        #Colocar um validador aqui
        self.auth_service.update_access_token_from_session_id(session_id, access_token)