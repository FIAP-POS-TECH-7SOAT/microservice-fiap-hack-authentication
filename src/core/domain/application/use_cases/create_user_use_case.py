from src.shared.logger import LoggerFactory
from src.adapters.drivers.http.dtos.create_user_request_dto import CreateUserRequest
from src.core.domain.application.services.user_service import UserService
from src.core.domain.validators.create_user_request_validator import CreateUserRequestValidator

from marshmallow import ValidationError

class CreateUserUseCase:
    def __init__(self, user_service: UserService):
        self.logger = LoggerFactory()
        self.user_service = user_service
        
        self.logger.info(f"CreateUserUseCase :: Constructor :: Declaring CreateUserRequestValidator")
        self.validator = CreateUserRequestValidator()

    def execute(self, user_request: CreateUserRequest) -> bool:
        """Executes the creation of user logic."""
        try:
            self.logger.info(f"CreateUserUseCase :: execute :: Validation of user model")
            self.validator.load(user_request.__dict__)
        except ValidationError as err:
            self.logger.error(f"CreateUserUseCase :: execute :: Invalid user model {err}")
            raise ValueError(f"Invalid data: {err.messages}")
        
        self.logger.info(f"CreateUserUseCase :: execute :: Validated user model")
        return self.user_service.register_user(user_request)
