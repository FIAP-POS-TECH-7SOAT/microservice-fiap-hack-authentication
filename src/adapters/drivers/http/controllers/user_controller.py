from flask import Blueprint, jsonify, request

from src.shared.logger import LoggerFactory
from src.adapters.drivers.http.dtos.create_user_request_dto import CreateUserRequest
from src.core.domain.application.use_cases.create_user_use_case import CreateUserUseCase
from src.core.domain.application.services.user_service import UserService


def user_bp(user_service: UserService):
    user_blueprint = Blueprint('user', __name__)
    logger = LoggerFactory()

    @user_blueprint.route("/user/create", methods=["POST"])
    def create_user():
        logger.info(f"UserController :: create_user :: Init route /user/create")
        try:
            logger.info(f"UserController :: create_user :: Declaring CreateUserUseCase")
            create_user_use_case = CreateUserUseCase(user_service)
            
            try:
                logger.info(f"UserController :: create_user :: Building user model")
                user = CreateUserRequest(
                    user_email = request.json['user_email'],
                    password = request.json['password'],
                    phone = request.json['phone'],
                )
            except Exception as ex:
                logger.error(f"UserController :: create_user :: Is missing {str(ex)}")
                return jsonify({"error": f"Is missing: {str(ex)}"}), 404

            try:
                logger.info(f"UserController :: create_user :: Executing create_user_use_case")
                result = create_user_use_case.execute(user)

                if result:
                    logger.info(f"UserController :: create_user :: User created")
                    return jsonify({'message': 'User created'}), 200
                else:
                    logger.error(f"UserController :: create_user :: User not created")
                    return jsonify({'message': 'User not created'}), 401

            except ValueError as ex:
                logger.error(f"UserController :: create_user :: Error {ex}")
                return jsonify({'message': f'{ex}'}), 401

        except Exception as ex:
            logger.error(f"UserController :: create_user :: Error {ex}")
            return jsonify({'message': 'Unable to process request'}), 500
        
    return user_blueprint
