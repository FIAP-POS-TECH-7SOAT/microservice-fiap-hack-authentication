
from src.adapters.drivens.infra.repositories.token_repository import TokenRepository
from src.adapters.drivens.infra.repositories.tracker_repository import TrackerRepository
from src.core.domain.application.services.Iauth_service import IAuthService
from src.core.domain.models.tracker_model import TrackUserAccess
from src.core.domain.models.token_model import Token

class AuthService(IAuthService):
    def __init__(self):
        self.token_repository = TokenRepository()
        self.tracker_repository = TrackerRepository()

    def insert_refresh_token(self, token:Token):
        """Insert a new token into database."""
        try:
            self.token_repository.delete_token(token.user_id)

            new_token = Token(
                session_id=token.session_id,
                user_id=token.user_id,
                access_token=token.access_token,
                refresh_token=token.refresh_token,
                expires_at=token.expires_at
            )
            
            track_access = TrackUserAccess(user_id=token.user_id)

            self.token_repository.save_token(new_token)
            self.tracker_repository.save_tracker(track_access)
        
        except:
            raise    

    def get_refresh_token(self, user_email: str)->dict[str]|None:
        """Get a new refreshed token in database"""
        try:
            token = self.token_repository.get_token_by_email(user_email)

            if token:
                return {
                    'SESSION_ID': token.session_id,
                    'ACCESS_TOKEN': token.access_token,
                    'REFRESH_TOKEN': token.refresh_token,
                    'EXPIRES_AT': token.expires_at
                }
            return None

        except:
            raise

    def update_access_token_from_session_id(self, session_id: str, access_token: str):
        """Update access token based on session"""
        try:
            token = self.token_repository.get_token_by_session(session_id)
            if token:
                token.access_token = access_token
                self.token_repository.save_token(token)
        
        except:
            raise