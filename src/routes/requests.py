from datetime import datetime
from flask import Blueprint, jsonify
from configs.app_settings import AppSettings
from providers.auth_provider import AuthProvider
from services.csc_service import CSCService
from services.user_service import UserService

requests_bp = Blueprint('requests', __name__)

@requests_bp.route('/catalog', methods=['GET'])
@AuthProvider.token_required(secret_key=AppSettings.SECRET_KEY_API)
def get_possible_requests(current_user):
    try:
        init = datetime.now()

        csc_service = CSCService()

        requests = csc_service.get_catalog_requests_csc()
        
        end = datetime.now()
        elapsed_time = end - init

        return jsonify({
            'data': requests
        }), 200

    except Exception as ex:
        return jsonify({
            'message': 'Unable to process request'
        }), 500
    
@requests_bp.route('/status', methods=['GET'])
@AuthProvider.token_required(secret_key=AppSettings.SECRET_KEY_API)
def get_requests_status(current_user):
    try:
        init = datetime.now()
        
        csc_service = CSCService()

        requests = csc_service.get_requests_csc_status_from_user(current_user['user'])

        end = datetime.now()
        elapsed_time = end - init

        return jsonify({
            'data': requests
        }), 200
    
    except Exception as ex:
        return jsonify({
            'message': 'Unable to process request'
        }), 500