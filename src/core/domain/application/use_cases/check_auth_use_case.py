from src.core.domain.validators.check_auth_request_validator import CheckAuthRequestValidator
from src.core.domain.application.services.auth_service import AuthService
from src.core.domain.application.ports.providers.dtos.auth_user_dto import AuthUser

from marshmallow import ValidationError

class CheckAuthUseCase:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.validator = CheckAuthRequestValidator()

    def execute(self, user_credentials: AuthUser) -> bool:
        """Executes the payment processing logic."""
        # try:
        #     self.validator.load(user_credentials.__dict__)
        # except ValidationError as err:
        #     raise ValueError(f"Invalid data: {err.messages}")
        
        return self.auth_service.authenticate_user(user_credentials)
