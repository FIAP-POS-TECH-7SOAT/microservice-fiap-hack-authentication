from datetime import datetime
from repository.token_repository import TokenRepository
from configs.app_settings import AppSettings

class UserService:
    def __init__(self):
        self.TokenRepository = TokenRepository()
    
    def set_refresh_token(self, session_id: str, user: str, access_token: str, refresh_token: str, expiration: datetime):
        try:
            self.TokenRepository.insert_refresh_token(session_id, user, access_token, refresh_token, expiration)
            
        except Exception as ex:
            raise

    def get_refresh_token(self, user: str):
        try:
            return self.TokenRepository.get_refresh_token(user)
        
        except Exception as ex:
            raise

    def update_access_token_from_session_id(self, session_id: str, access_token: str):
        try:
            self.TokenRepository.update_access_token_from_session_id(session_id, access_token)
        
        except Exception as ex:
            raise