from src.shared.logger import LoggerFactory
from src.adapters.drivers.http.dtos.token_request_dto import TokenRequest
from src.core.domain.application.services.auth_service import AuthService
from src.core.domain.validators.token_request_validator import TokenValidator

from marshmallow import ValidationError

class VerifyTokenUseCase:
    def __init__(self, auth_service: AuthService):
        self.logger = LoggerFactory()
        self.auth_service = auth_service
        
        self.logger.info("VerifyTokenUseCase :: Constructor :: Declaring TokenValidator")
        self.validator = TokenValidator()

    def execute(self, token: TokenRequest) -> dict:
        """Executes the verification of token logic."""
        try:
            self.logger.info("VerifyTokenUseCase :: execute :: Validate token data")
            self.validator.load(token.__dict__)
        except ValidationError as err:
            self.logger.error(f"VerifyTokenUseCase :: execute :: Error {err}")
            raise ValueError(f"Validate data error: {err.messages}")
        
        self.logger.info("VerifyTokenUseCase :: execute :: Validate token data conclued")
        return self.auth_service.verify_token(token)
