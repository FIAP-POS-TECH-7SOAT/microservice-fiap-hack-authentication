from src.core.domain.application.ports.repositories.Itoken_repository import ITokenRepository
from src.adapters.drivens.infra.database.config import db
from src.core.domain.models.token_model import Token

from sqlalchemy.exc import SQLAlchemyError

class TokenRepository(ITokenRepository):
    def __init__(self):
        self.db = db
        
    def save_token(self, token:Token):
        try:
            self.db.session.add(token)
            self.db.session.commit()
            
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise

    def get_token_by_email(self, user_email:str)->Token:
        try:
            return Token.query.filter_by(user_id=user_email).first()

        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise
        
    def get_token_by_session(self, session_id:str)->Token:
        try:
            return Token.query.filter_by(session_id=session_id).first()

        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise
        
    def delete_token(self, user_email:str):
        try:
            Token.query.filter_by(user_id=user_email).delete()
            self.db.session.commit()
        
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise

    def update_token(self, session_id: str, access_token: str):
        try:
            token:Token = self.get_token_by_email(session_id)
            if token:
                token.access_token = access_token
                self.db.session.commit()

        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise