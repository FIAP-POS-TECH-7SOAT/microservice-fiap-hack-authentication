import bcrypt

from src.shared.logger import LoggerFactory
from src.adapters.drivers.http.dtos.create_user_request_dto import CreateUserRequest
from src.adapters.drivens.infra.repositories.user_repository import UserRepository
from src.core.domain.application.services.Iuser_service import IUserService
from src.core.domain.models.user_model import User

class UserService(IUserService):
    def __init__(self):
        self.logger = LoggerFactory()
        
        self.logger.info(f"UserService :: Constructor :: Declaring UserRepository")
        self.user_repository = UserRepository()

    def register_user(self, user_request:CreateUserRequest)->bool:
        """Register a new user with a hashed password."""
        try:
            self.logger.info(f"UserService :: register_user :: Getting user {user_request.user_email}")
            user = self.user_repository.get_user(user_request.user_email)
            
            if user:
                self.logger.error(f"UserService :: register_user :: Error User already exists")
                raise ValueError("User already exists")
            
            self.logger.info(f"UserService :: register_user :: Generating salt")
            salt = bcrypt.gensalt()
            
            self.logger.info(f"UserService :: register_user :: Hashing password")
            hashed_password = bcrypt.hashpw(user_request.password.encode("utf-8"), salt).decode("utf-8")
            
            self.logger.info(f"UserService :: register_user :: Creating User Model")
            user = User(
                user_email = user_request.user_email,
                password = hashed_password,
                phone = user_request.phone
            )
            
            self.logger.info(f"UserService :: register_user :: Saving user into Database")
            self.user_repository.save_user(user)
            
            return True
        
        except Exception as err:
            self.logger.error(f"UserService :: register_user :: Error {err}")
            raise ValueError(f"Invalid data: {err}")
        
    def delete_user(self, user_email: str)->str:
        """Delete user"""
        try:
            self.logger.info(f"UserService :: delete_user :: Getting user from {user_email}")
            user = self.user_repository.get_user(user_email)
            if not user:
                self.logger.error(f"UserService :: delete_user :: User does not exist")
                raise ValueError("User does not exist")
            
            self.logger.info(f"UserService :: delete_user :: Deleting user {user_email}")
            self.user_repository.delete_user(user_email)
            
            self.logger.info(f"UserService :: delete_user :: User {user_email} deleted")
            return f"User {user_email} deleted!"
            
        except Exception as ex:
            self.logger.error(f"UserService :: delete_user :: Error {ex}")
            raise ValueError(str(ex))