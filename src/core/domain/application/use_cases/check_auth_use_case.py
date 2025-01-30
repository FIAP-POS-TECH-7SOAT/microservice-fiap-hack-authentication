from src.shared.logger import LoggerFactory
from src.adapters.drivers.http.dtos.auth_user_dto import AuthUser
from src.core.domain.validators.check_auth_request_validator import CheckAuthRequestValidator
from src.core.domain.application.services.auth_service import AuthService


from marshmallow import ValidationError

class CheckAuthUseCase:
    def __init__(self, auth_service: AuthService):
        self.logger = LoggerFactory()
        self.auth_service = auth_service
        
        self.logger.info(f"CheckAuthUseCase :: Constructor :: Declaring CheckAuthRequestValidator")
        self.validator = CheckAuthRequestValidator()

    def execute(self, user_credentials: AuthUser) -> str:
        """Executes the authenticate logic."""
        try:
            self.logger.info(f"CheckAuthUseCase :: execute :: Validation user credentials object")
            self.validator.load(user_credentials.__dict__)
        except ValidationError as err:
            self.logger.error(f"CheckAuthUseCase :: execute :: Error {err}")
            raise ValueError(f"Invalid data: {err.messages}")
        
        self.logger.info(f"CheckAuthUseCase :: execute :: Validated user credentials object")
        return self.auth_service.authenticate_user(user_credentials)
