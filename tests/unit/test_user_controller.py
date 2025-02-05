import unittest
from unittest.mock import MagicMock
from flask import Flask
from itsdangerous import URLSafeTimedSerializer

from src.adapters.drivers.http.controllers.user_controller import user_bp
from src.core.domain.application.services.user_service import UserService
from src.adapters.drivens.infra.settings.env import ENV

class TestUserController(unittest.TestCase):
    def setUp(self):
        self.mock_user_service = MagicMock(spec=UserService)
        self.app = Flask(__name__)
        self.app.register_blueprint(user_bp(self.mock_user_service))
        self.client = self.app.test_client()
        
        self.mock_env = MagicMock(spec=ENV)
        self.env = ENV()
        self.serializer = URLSafeTimedSerializer(self.env.SALT_KEY)
        self.test_email = "test_user@gmail.com"
        self.token = self.serializer.dumps(self.test_email, salt=self.env.SALT_KEY)

    def test_create_user_success(self):
        payload = {
            "user_email": "test_user@gmail.com",
            "password": "plain_password",
            "phone": "+551112347896"
        }

        self.mock_user_service.register_user.return_value = True

        response = self.client.post('/user/create', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertIn("User created", response.json["message"])

    def test_create_user_already_exists(self):
        payload = {
            "user_email": "test_user@gmail.com",
            "password": "plain_password",
            "phone": "+551112347896"
        }

        self.mock_user_service.register_user.side_effect = ValueError("User already exists")

        response = self.client.post('/user/create', json=payload)

        self.assertEqual(response.status_code, 401)
        self.assertIn("User already exists", response.json["message"])
        
    def test_verify_email_success(self):
        self.mock_user_service.get_user_by_email.return_value = {"email": self.test_email}
        
        response = self.client.get(f'/user/verify/{self.token}')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Email verified successfully!", response.json["message"])

    def test_verify_email_user_not_found(self):
        self.mock_user_service.get_user_by_email.return_value = None
        
        response = self.client.get(f'/user/verify/{self.token}')
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json["message"])

    def test_verify_email_invalid_or_expired_token(self):
        invalid_token = "invalid_token"
        
        response = self.client.get(f'/user/verify/{invalid_token}')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid or expired token", response.json["message"])



