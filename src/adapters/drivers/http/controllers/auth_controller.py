from flask import Blueprint, jsonify, request

from src.core.domain.application.ports.providers.dtos.token_request_dto import TokenRequest
from src.core.domain.application.use_cases.verify_token_use_case import VerifyTokenUseCase
from src.core.domain.application.ports.providers.dtos.auth_user_dto import AuthUser
from src.core.domain.application.use_cases.check_auth_use_case import CheckAuthUseCase
from src.core.domain.application.services.auth_service import AuthService


def auth_bp(auth_service: AuthService):
    auth_blueprint = Blueprint('auth', __name__)

    @auth_blueprint.route("/auth/check", methods=["POST"])
    def check_auth():
        try:
            check_auth_use_case = CheckAuthUseCase(auth_service)
            
            try:
                auth_user = AuthUser(
                    user_email = request.json['email'],
                    password = request.json['password'],
                )
                
            except Exception as ex:
                return jsonify({"error": f"Is missing: {str(ex)}"}), 404

            try:
                result = check_auth_use_case.execute(auth_user)
                
                if result:
                    return jsonify({'token': result}), 200
                else:
                    return jsonify({'message': 'Something went wrong'}), 401

            except:
                return jsonify({'message': 'Invalid data'}), 401

        except Exception as ex:
            return jsonify({'message': 'Unable to process request'}), 500
        
    
    @auth_blueprint.route("/auth/verify", methods=["POST"])
    def verify_token():
        try:
            verify_token_use_case = VerifyTokenUseCase(auth_service)
            
            try:
                token = TokenRequest(
                    token=request.json['token']
                )
                
            except Exception as ex:
                return jsonify({"error": f"Is missing: {str(ex)}"}), 404

            try:
                result = verify_token_use_case.execute(token)
                
                if result:
                    return jsonify({'payload': result}), 200
                else:
                    return jsonify({'message': 'Something went wrong'}), 401

            except:
                return jsonify({'message': 'Invalid data'}), 401

        except Exception as ex:
            return jsonify({'message': 'Unable to process request'}), 500


    return auth_blueprint
