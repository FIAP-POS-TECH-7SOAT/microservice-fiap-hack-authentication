from flask import Blueprint, jsonify, request
from itsdangerous import URLSafeTimedSerializer

from src.core.domain.application.services.email_service import MailSend
from src.adapters.drivens.infra.settings.env import ENV
from src.shared.logger import LoggerFactory
from src.adapters.drivers.http.dtos.create_user_request_dto import CreateUserRequest
from src.core.domain.application.use_cases.create_user_use_case import CreateUserUseCase
from src.core.domain.application.services.user_service import UserService


def user_bp(user_service: UserService):
    user_blueprint = Blueprint('user', __name__)
    logger = LoggerFactory()
    env = ENV()
    serializer = URLSafeTimedSerializer(env.SALT_KEY)
    sender = MailSend()

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
                    logger.info(f"UserController :: create_user :: User created {user.user_email}")
                    
                    logger.info(f"UserController :: create_user :: Generating token")
                    token = serializer.dumps(user.user_email, salt=env.SALT_KEY)
                    
                    logger.info(f"UserController :: create_user :: Creating url to verify email {user.user_email}")
                    verification_url = f"{env.BASE_URL}/user/verify/{token}"
                    # verification_url = url_for('user.verify_email', token=token, _external=True)
                    
                    logger.info(f"UserController :: create_user :: Building email body and subject")
                    body = f"Click para verificar o email: {verification_url}"
                    subject = "Verificação de Email"
                    
                    logger.info(f"UserController :: create_user :: Sending Email")
                    sender.send_email(user.user_email, subject, body)
                    
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
        
    @user_blueprint.route("/user/verify/<token>", methods=["GET"])
    def verify_email(token):
        try:
            logger.info(f"UserController :: verify_email :: Getting user email")
            user_email = serializer.loads(token, salt=env.SALT_KEY, max_age=3600)
            
            logger.info(f"UserController :: verify_email :: Getting user by email {user_email}")
            user = user_service.get_user_by_email(user_email)
            
            if not user:
                logger.error(f"UserController :: verify_email :: User not found")
                return jsonify({"message": "User not found"}), 404
            
            logger.info(f"UserController :: verify_email :: User verify")
            user_service.user_verify(user)

            logger.info(f"UserController :: verify_email :: User verified")
            return jsonify({"message": "Email verified successfully!"}), 200

        except Exception:
            logger.error(f"UserController :: verify_email :: Invalid or expired token")
            return jsonify({"message": "Invalid or expired token"}), 400
        
    return user_blueprint
