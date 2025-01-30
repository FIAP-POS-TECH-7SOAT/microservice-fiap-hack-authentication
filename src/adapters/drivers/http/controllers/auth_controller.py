from flask import Blueprint, jsonify, request

from src.shared.logger import LoggerFactory
from src.adapters.drivers.http.dtos.token_request_dto import TokenRequest
from src.adapters.drivers.http.dtos.auth_user_dto import AuthUser
from src.core.domain.application.use_cases.verify_token_use_case import VerifyTokenUseCase
from src.core.domain.application.use_cases.check_auth_use_case import CheckAuthUseCase
from src.core.domain.application.services.auth_service import AuthService


def auth_bp(auth_service: AuthService):
    auth_blueprint = Blueprint('auth', __name__)
    logger = LoggerFactory()

    @auth_blueprint.route("/auth/check", methods=["POST"])
    def check_auth():
        logger.info(f"AuthController :: check_auth :: Init route /auth/check")
        try:
            logger.info(f"AuthController :: check_auth :: Declaring CheckAuthUseCase")
            check_auth_use_case = CheckAuthUseCase(auth_service)
            
            try:
                logger.info(f"AuthController :: check_auth :: Build AuthUser object")
                auth_user = AuthUser(
                    user_email = request.json['user_email'],
                    password = request.json['password'],
                )
                logger.info(f"AuthController :: check_auth :: Authentication of user {request.json['user_email']}")
                
            except Exception as ex:
                logger.error(f"AuthController :: check_auth :: Error {ex}")
                return jsonify({"error": f"Is missing: {str(ex)}"}), 404

            try:
                logger.info(f"AuthController :: check_auth :: Executing check_auth_use_case")
                result = check_auth_use_case.execute(auth_user)
                
                if result:
                    logger.info(f"AuthController :: check_auth :: Returning token")
                    return jsonify({'token': result}), 200
                else:
                    logger.error(f"AuthController :: check_auth :: Error {result}")
                    return jsonify({'message': 'Something went wrong'}), 401

            except Exception as ex:
                logger.error(f"AuthController :: check_auth :: Error {ex}")
                return jsonify({'message': f'{ex}'}), 401

        except Exception as ex:
            logger.info(f"AuthController :: check_auth :: Error {ex}")
            return jsonify({'message': 'Unable to process request'}), 500
        
    
    @auth_blueprint.route("/auth/verify", methods=["POST"])
    def verify_token():
        logger.info(f"AuthController :: verify_token :: Init route /auth/verify")
        try:
            logger.info(f"AuthController :: verify_token :: Declaring VerifyTokenUseCase")
            verify_token_use_case = VerifyTokenUseCase(auth_service)
            
            try:
                logger.info(f"AuthController :: verify_token :: Building TokenRequest object")
                token = TokenRequest(
                    token = request.json['token'],
                )
                
            except Exception as ex:
                logger.error(f"AuthController :: verify_token :: Error {ex}")
                return jsonify({"error": f"Is missing: {str(ex)}"}), 404

            try:
                logger.info(f"AuthController :: verify_token :: Executing verification of token")
                result = verify_token_use_case.execute(token)
                
                if result:
                    logger.info(f"AuthController :: verify_token :: Returning info user {result}")
                    return jsonify({'payload': result}), 200
                else:
                    logger.error(f"AuthController :: verify_token :: Error {result}")
                    return jsonify({'message': 'Something went wrong'}), 401

            except Exception as ex:
                logger.error(f"AuthController :: verify_token :: Error {ex}")
                return jsonify({'message': f'{ex}'}), 401

        except Exception as ex:
            logger.error(f"AuthController :: verify_token :: Error {ex}")
            return jsonify({'message': 'Unable to process request'}), 500


    return auth_blueprint
