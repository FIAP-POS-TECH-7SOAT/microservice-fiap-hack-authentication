from datetime import datetime
import hashlib
import time
import uuid
from flask import Blueprint, jsonify, make_response, redirect, request
import requests
from configs.app_settings import AppSettings
from providers.auth_provider import AuthProvider
from services.user_service import UserService

oauth_bp = Blueprint('oauth', __name__)

@oauth_bp.route('/callback', methods=['GET'])
def oauth_callback():
    try:
        init = datetime.now()

        ip_address = request.remote_addr

        user_agent = request.headers.get('User-Agent').strip()

        user_service = UserService()
        
        code = request.args.get('code')

        if not code:
            return jsonify({
                    'message': 'Authorization code is missing'
                }), 400

        token_response = requests.post(
            AppSettings.OAUTH_URL, 
            data={
                'grant_type': AppSettings.OAUTH_GRANT_TYPE,
                'code': code,
                'redirect_uri': AppSettings.OAUTH_REDIRECT_URL,
                'client_id': AppSettings.OAUTH_CLIENT_ID,
                'client_secret': AppSettings.OAUTH_CLIENT_SECRET,
            }
        )

        if token_response.status_code == 200:
            tokens = token_response.json()

            max_retries = 3
            for attempt in range(max_retries):
                
                user_info_response = requests.get(
                    AppSettings.OAUTH_USER_INFO, 
                    headers={
                        "Authorization": f"Bearer {tokens['access_token']}"
                    }
                )

                if user_info_response.status_code == 200:
                    
                    user_info_json = user_info_response.json()

                    email = user_info_json['userid']

                    tk_result = AuthProvider.generate_token_jwt(
                        email, 
                        AppSettings.SECRET_KEY_API
                    )

                    refresh_tk_result = AuthProvider.generate_refresh_token_jwt(
                        email, 
                        AppSettings.SECRET_KEY_API
                    )

                    session_uuid = uuid.uuid4()

                    hashed_user_agent = hashlib.sha256(user_agent.encode()).hexdigest()
                    user_service.set_refresh_token(
                        AuthProvider.generate_pass_hash(f"{session_uuid}||{hashed_user_agent}||{ip_address}"),
                        refresh_tk_result.user,
                        AuthProvider.hash_for_jwt_token(tk_result.token), 
                        refresh_tk_result.token, 
                        refresh_tk_result.expiration)

                    response = make_response(
                        redirect(AppSettings.URL_FINANCE_GATEWAY)
                    )
                    
                    response.set_cookie('session_id', str(session_uuid), httponly=True, secure=True, samesite='Lax')
                    response.set_cookie('tk', tk_result.token, httponly=True, secure=True, samesite='Lax')
                    
                    end = datetime.now()
                    elapsed_time = end - init

                    return response

                elif attempt < max_retries - 1:
                    time.sleep(1)

                else:
                    return jsonify({
                        'message': 'Failure to validate user information'
                    }), 500

        else:
            return jsonify({
                'message': 'Failed to retrieve token'
            }), 500
        
    except Exception as ex:
        return jsonify({
            'message': 'We were unable to process your request'
        }), 500
