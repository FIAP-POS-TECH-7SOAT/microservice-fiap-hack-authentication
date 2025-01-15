import datetime
from functools import wraps
import hashlib

from src.core.domain.application.ports.providers.dtos.token_result_dto import TokenResult

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify

class AuthProvider:
    @staticmethod
    def hash_for_jwt_token(token: str):
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def generate_token_jwt(user_email: str, secret: str) -> TokenResult:
        expiration = datetime.datetime.now() + datetime.timedelta(minutes=10)

        token = jwt.encode({
            'user': user_email,
            'expiration': expiration.timestamp()
        }, secret, algorithm='HS256')

        result = TokenResult(
            user=user_email, 
            token=token, 
            expiration=expiration
        )
        return result
    
    @staticmethod
    def generate_refresh_token_jwt(user_email: str, secret: str) -> TokenResult:
        expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        
        token = jwt.encode({
            'user': user_email,
            'expiration': expiration.timestamp()
        }, secret, algorithm='HS256')

        result = TokenResult(
            user=user_email, 
            token=token, 
            expiration=expiration
        )
        return result

    @staticmethod
    def generate_pass_hash(password: str):
        return generate_password_hash(password)

    @staticmethod
    def check_pass_hash(hash: str, password: str):
        return check_password_hash(hash, password)
    
    @staticmethod
    def session_required(secret_key: str):
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                session_uuid = request.cookies.get('session_id', "")

                if not session_uuid or session_uuid == "":
                    return jsonify({
                        'message': 'Session Token is missing!'
                    }), 401
                
                access_token = request.cookies.get('tk', "")
                if not access_token or access_token == "":
                    return jsonify({
                        'message': 'Access Token is missing!'
                    }), 401

                try:
                    data = jwt.decode(access_token, secret_key, algorithms=["HS256"])
                    current_user = data['user']
                    
                    ip_address = request.remote_addr

                    user_agent = request.headers.get('User-Agent', "").strip()

                    hashed_user_agent = hashlib.sha256(user_agent.encode()).hexdigest()
                    session_id_hash = f"{session_uuid}||{hashed_user_agent}||{ip_address}"

                except jwt.ExpiredSignatureError:
                    return jsonify({
                        'message': 'Token has expired!'
                    }), 401
                
                except jwt.InvalidTokenError:
                    return jsonify({
                        'message': 'Invalid token!'
                    }), 401

                return f(current_user, session_uuid, session_id_hash, access_token, *args, **kwargs)
            return decorated
        return decorator

    
    @staticmethod
    def token_required(secret_key: str):
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                session_id = None
                if 'session_id' in request.cookies:
                    session_id = request.cookies['session_id']

                if not session_id:
                    return jsonify({
                        'message': 'Session Token is missing!'
                    }), 401
                
                access_token = None
                if 'tk' in request.cookies:
                    access_token = request.cookies['tk']

                if not access_token:
                    return jsonify({
                        'message': 'Access Token is missing!'
                    }), 401
                
                try:
                    data = jwt.decode(access_token, secret_key, algorithms=["HS256"])
                    current_user = {
                        'user': data['user']
                    }

                    expiration = datetime.datetime.fromtimestamp(data['expiration'])
                    current_time = datetime.datetime.now()

                    if current_time > expiration:
                        return jsonify({
                            'message': 'Token has expired!'
                        }), 401

                except jwt.ExpiredSignatureError:
                    return jsonify({
                        'message': 'Token has expired!'
                    }), 401
                
                except jwt.InvalidTokenError:
                    return jsonify({
                        'message': 'Invalid token!'
                    }), 401
                
                return f(current_user, *args, **kwargs)
            return decorated
        return decorator