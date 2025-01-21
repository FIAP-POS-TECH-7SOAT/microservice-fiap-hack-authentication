from src.adapters.drivers.http.dtos.token_request_dto import TokenRequest
from src.core.domain.application.services.auth_service import AuthService
from src.core.domain.validators.token_request_validator import TokenValidator

from marshmallow import ValidationError

class VerifyTokenUseCase:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.validator = TokenValidator()

    def execute(self, token: TokenRequest) -> bool:
        """Executes the payment processing logic."""
        try:
            self.validator.load(token.__dict__)
        except ValidationError as err:
            raise ValueError(f"Invalid data: {err.messages}")
        
        return self.auth_service.verify_token(token)
