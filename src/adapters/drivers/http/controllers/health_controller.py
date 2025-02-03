from flask import Blueprint, jsonify

def health_bp():
    health_blueprint = Blueprint('health', __name__)

    @health_blueprint.route("/health", methods=["GET"])
    def check_health_server():
        try:
            return jsonify({'message': "Page Loaded"}), 200
            
        except:
            return jsonify({'message': 'Unable to process request'}), 500
        
    return health_blueprint