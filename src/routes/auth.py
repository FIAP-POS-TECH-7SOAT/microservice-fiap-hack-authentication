from datetime import datetime
from flask import Blueprint, jsonify, make_response, request
import jwt
from configs.app_settings import AppSettings
from providers.auth_provider import AuthProvider
from services.user_service import UserService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/check-auth', methods=['GET'])
@AuthProvider.token_required(secret_key=AppSettings.SECRET_KEY_API)
def check_auth(current_user):
    try:
        return jsonify({
            'message': 'User is authenticated', 
            'user': current_user['user']
        }), 200
    
    except Exception as ex:
        return jsonify({
            'message': 'Unable to process request'
        }), 500
    
@auth_bp.route('/refresh-token', methods=['GET'])
@AuthProvider.session_required(secret_key=AppSettings.SECRET_KEY_API)
def refresh_token(current_user, session_uuid, session_id, access_token):
    try:
        init = datetime.now()

        user_service = UserService()
        credentials = user_service.get_refresh_token(current_user)
        
        if not credentials or len(credentials) == 0:
            return jsonify({
                'message': 'credentials not found for user'
            }), 401

        session_id_db_encrypted = credentials[0]['SESSION_ID']
        last_access_token_encrypted = credentials[0]['ACCESS_TOKEN']
        refresh_token = credentials[0]['REFRESH_TOKEN']

        has_valid_session = AuthProvider.check_pass_hash(session_id_db_encrypted, session_id)
        has_a_last_access_token_valid = (last_access_token_encrypted == AuthProvider.hash_for_jwt_token(access_token))

        if not has_valid_session or not has_a_last_access_token_valid:
            return jsonify({
                'message': 'Invalid Session'
            }), 401

        try:
            data = jwt.decode(
                refresh_token, 
                AppSettings.SECRET_KEY_API, 
                algorithms=["HS256"]
            )


            expiration = datetime.fromtimestamp(data['expiration'])
            current_time = datetime.now()

            if current_time > expiration:
                return jsonify({
                    'message': 'Refresh Token has expired!'
                }), 401
            

            new_access_token_result = AuthProvider.generate_token_jwt(
                data['user'], 
                AppSettings.SECRET_KEY_API
            )

            user_service.update_access_token_from_session_id(
                session_id_db_encrypted,
                AuthProvider.hash_for_jwt_token(new_access_token_result.token)
            )


            resp = make_response(
                    jsonify({
                        'access_token': new_access_token_result.token
                    })
                )
            
            resp.set_cookie('session_id', session_uuid, httponly=False, secure=False, samesite='Lax')
            resp.set_cookie('tk', new_access_token_result.token, httponly=False, secure=False, samesite='Lax')

            end = datetime.now()
            elapsed_time = end - init

            return resp

        except jwt.ExpiredSignatureError:
            return jsonify({
                'message': 'Refresh token has expired'
            }), 401
        
        except jwt.InvalidTokenError:
            return jsonify({
                'message': 'Invalid refresh token'
            }), 401
        
    except Exception as ex:
        return jsonify({
            'message': 'Unable to process request'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        init = datetime.now()
        resp = make_response(jsonify({
            "message": "Logged out"
        }))

        resp.set_cookie('tk', '', httponly=True, secure=True, samesite='None')
        resp.set_cookie('session_id', '', httponly=True, secure=True, samesite='None')

        end = datetime.now()
        elapsed_time = end - init

        return resp
    
    except Exception as ex:
        return jsonify({
            'message': 'Unable to process request'
        }), 500