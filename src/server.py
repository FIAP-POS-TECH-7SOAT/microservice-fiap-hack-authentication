from flask import Flask
from flask_cors import CORS
from setup import setup
from routes.health import health_bp
from routes.oauth import oauth_bp
from routes.auth import auth_bp
from routes.requests import requests_bp

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["10.101.5.52"])

    setup()

    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(oauth_bp, url_prefix='/api/oauth')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(requests_bp, url_prefix='/api/requests')

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
