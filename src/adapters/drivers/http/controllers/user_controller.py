from flask import Blueprint, jsonify, request

from src.core.domain.application.ports.providers.dtos.create_user_request_dto import CreateUserRequest
from src.core.domain.application.use_cases.create_user_use_case import CreateUserUseCase
from src.core.domain.application.services.user_service import UserService


def user_bp(user_service: UserService):
    user_blueprint = Blueprint('user', __name__)

    @user_blueprint.route("/user/create", methods=["POST"])
    def create_user():
        try:
            create_user_use_case = CreateUserUseCase(user_service)
            
            try:
                user = CreateUserRequest(
                    user_email = request.json['email'],
                    password = request.json['password'],
                    phone = request.json['phone'],
                )
            except Exception as ex:
                return jsonify({"error": f"Is missing: {str(ex)}"}), 404

            try:
                result = create_user_use_case.execute(user)
                
                if result:
                    return jsonify({'message': 'User created'}), 200
                else:
                    return jsonify({'message': 'User not created'}), 401

            except:
                return jsonify({'message': 'Invalid data'}), 401

        except Exception as ex:
            return jsonify({'message': 'Unable to process request'}), 500
