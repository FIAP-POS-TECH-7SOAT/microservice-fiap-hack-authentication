from src.adapters.drivers.http.dtos.create_user_request_dto import CreateUserRequest
from src.core.domain.application.services.user_service import UserService
from src.core.domain.validators.create_user_request_validator import CreateUserRequestValidator

from marshmallow import ValidationError

class CreateUserUseCase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.validator = CreateUserRequestValidator()

    def execute(self, user_request: CreateUserRequest) -> bool:
        """Executes the payment processing logic."""
        try:
            self.validator.load(user_request.__dict__)
        except ValidationError as err:
            raise ValueError(f"Invalid data: {err.messages}")
        
        return self.user_service.register_user(user_request)
