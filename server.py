from flask import Flask

from src.adapters.drivers.http.controllers.health_controller import health_bp
from src.adapters.drivers.http.controllers.auth_controller import auth_bp
from src.adapters.drivers.http.controllers.user_controller import user_bp
from src.adapters.drivens.infra.settings.env import ENV
from src.adapters.drivens.infra.database.config import db
from src.core.domain.application.services.user_service import UserService
from src.core.domain.application.services.auth_service import AuthService
from src.shared.logger import LoggerFactory

logger = LoggerFactory()

logger.info("Server :: main :: Starting Flask")
app = Flask(__name__)

logger.info("Server :: main :: Calling ENV")
env = ENV()

logger.info("Server :: main :: Setting Database")
app.config['SQLALCHEMY_DATABASE_URI'] = env.CONNECT_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger.info("Server :: main :: Database linked to app")
db.init_app(app)

logger.info("Server :: main :: Declaring AuthService")
auth_service = AuthService()

logger.info("Server :: main :: Declaring UserService")
user_service = UserService()

logger.info("Server :: main :: Settings routes")
app.register_blueprint(auth_bp(auth_service))
app.register_blueprint(user_bp(user_service))
app.register_blueprint(health_bp())
# from src.adapters.drivers.http.controllers.password_controller import password_recovery_bp
# app.register_blueprint(password_recovery_bp())

if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()
            logger.info("Server :: main :: Database initialized successfully!")
    except Exception as ex:
        logger.info(f"Server :: main :: Error initializing database: {str(ex)}")
     
    logger.info(f"Server :: main :: Starting Server on PORT: {env.PORT}")    
    app.run(host='0.0.0.0', debug=True, port=env.PORT)
