from flask import Blueprint, jsonify, request
from itsdangerous import URLSafeTimedSerializer

from src.shared.logger import LoggerFactory
from src.core.domain.application.services.email_service import MailSend
from src.core.domain.application.services.user_service import UserService
from src.adapters.drivens.infra.settings.env import ENV

def password_recovery_bp(user_service: UserService, secret_key: str):
    password_recovery_blueprint = Blueprint('password_recovery', __name__)
    serializer = URLSafeTimedSerializer(secret_key)
    logger = LoggerFactory()
    env = ENV()
    sender = MailSend()
    
    @password_recovery_blueprint.route("/password/recover", methods=["POST"])
    def recover_password():
        try:
            logger.info(f"PasswordController :: recover_password :: Getting User Email")
            user_email = request.json['user_email']
            
            if not user_email:
                logger.error(f"PasswordController :: recover_password :: Email is not retrieved")
                return jsonify({"error": "Email is required"}), 400

            logger.info(f"PasswordController :: recover_password :: Getting user by email")
            user = user_service.get_user_by_email(user_email)
            if not user:
                logger.error(f"PasswordController :: recover_password :: User not found")
                return jsonify({"error": "User not found"}), 404

            logger.info(f"PasswordController :: recover_password :: Generating token")
            token = serializer.dumps(user_email, salt=env.SALT_KEY)
            
            logger.info(f"PasswordController :: recover_password :: Creating url and body to send in email")
            recovery_url = f"{env.BASE_URL}/password/reset/{token}"
            body = f"""Clique no link {recovery_url} para recuperar a senha"""
            
            logger.info(f"PasswordController :: recover_password :: Sending Email")
            sender.send_email(user_email, "Recuperação de Senha", body)

            return jsonify({"message": "Recovery email sent"}), 200

        except Exception as ex:
            logger.error(f"PasswordController :: recover_password :: Error Unable to process request - {ex}")
            return jsonify({"error": f"Unable to process request: {str(ex)}"}), 500

    @password_recovery_blueprint.route("/password/reset/<token>", methods=["POST"])
    def reset_password(token):
        try:
            logger.info(f"PasswordController :: reset_password :: Getting new password")
            new_password = request.json['new_password']
            if not new_password:
                logger.error(f"PasswordController :: reset_password :: password not passed")
                return jsonify({"error": "New password is required"}), 400

            try:
                logger.info(f"PasswordController :: reset_password :: Verifying token to get user_email")
                user_email:str = serializer.loads(token, salt=env.SALT_KEY, max_age=3600)

            except Exception:
                logger.error(f"PasswordController :: reset_password :: Invalid or expired token")
                return jsonify({"error": "Invalid or expired token"}), 400

            logger.info(f"PasswordController :: reset_password :: Get user by email {user_email}")
            user = user_service.get_user_by_email(user_email)
            if not user:
                logger.info(f"PasswordController :: reset_password :: User not found")
                return jsonify({"error": "User not found"}), 404

            logger.info(f"PasswordController :: reset_password :: Updating password from user {user_email}")
            user_service.update_password(user.user_email, new_password)
            return jsonify({"message": "Password reset successful"}), 200

        except Exception as ex:
            return jsonify({"error": f"Unable to process request: {str(ex)}"}), 500

    return password_recovery_blueprint
