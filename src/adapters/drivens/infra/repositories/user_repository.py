from src.shared.logger import LoggerFactory
from src.adapters.drivens.infra.database.config import db
from src.core.domain.models.user_model import User
from src.core.domain.application.ports.repositories.Iuser_repository import IUserRepository
from sqlalchemy.exc import SQLAlchemyError

class UserRepository(IUserRepository):
    def __init__(self):
        self.db = db
        self.logger = LoggerFactory()
        
    def save_user(self, user:User):
        try:
            self.db.session.add(user)
            self.db.session.commit()
            
        except SQLAlchemyError as e:
            self.logger.error(f"UserRepository :: save_user :: Error {e}")
            self.db.session.rollback()
            raise

    def get_user(self, user_email:str)->User:
        try:
            return User.query.filter_by(user_email=user_email).first()

        except SQLAlchemyError as e:
            self.logger.error(f"UserRepository :: get_user :: Error {e}")
            self.db.session.rollback()
            raise
        
    def delete_user(self, user_email:str):
        try:
            user = self.get_user(user_email)
            if user:
                user.active = False
                self.db.session.commit()
        
        except SQLAlchemyError as e:
            self.logger.error(f"UserRepository :: delete_user :: Error {e}")
            self.db.session.rollback()
            raise

    def update_password(self, user_email: str, password:str):
        try:
            user = self.get_user(user_email)
            if user:
                user.password = password
                self.db.session.commit()

        except SQLAlchemyError as e:
            self.logger.error(f"UserRepository :: update_password :: Error {e}")
            self.db.session.rollback()
            raise