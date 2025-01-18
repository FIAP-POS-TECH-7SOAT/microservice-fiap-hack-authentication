import bcrypt

from src.core.domain.application.ports.providers.dtos.create_user_request_dto import CreateUserRequest
from src.adapters.drivens.infra.repositories.user_repository import UserRepository
from src.core.domain.application.services.Iuser_service import IUserService
from src.core.domain.models.user_model import User

class UserService(IUserService):
    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, user_request:CreateUserRequest)->bool:
        """Register a new user with a hashed password."""
        try:
            
            user = self.user_repository.get_user(user_request.user_email)
            if user:
                raise ValueError("User already exists")
            
            hashed_password = bcrypt.hashpw(user_request.password.encode(), bcrypt.gensalt())
            
            user = User(
                user_email = user_request.user_email,
                password = hashed_password,
                phone = user_request.phone
            )
            
            self.user_repository.save_user(user)
            
            return True
        
        except:
            raise

    def update_password(self, user_email: str, password:str, new_password:str)->bool:
        """Update password from user - Need current password"""
        try:
            user = self.user_repository.get_user(user_email)
            if not user:
                raise ValueError("User does not exist")
            
            hashed_password = user.password
            if not bcrypt.checkpw(password.encode(), hashed_password):
                raise ValueError("Invalid credentials")
            
            new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            
            self.user_repository.update_password(user_email, new_hashed_password)
            
            return True

        except:
            raise
        
    def delete_user(self, user_email: str)->str:
        """Delete user"""
        try:
            user = self.user_repository.get_user(user_email)
            if not user:
                raise ValueError("User does not exist")
            
            self.user_repository.delete_user(user_email)
            
            return f"User {user_email} deleted!"
            
        except:
            raise