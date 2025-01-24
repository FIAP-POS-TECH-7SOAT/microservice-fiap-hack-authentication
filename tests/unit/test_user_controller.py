import unittest
from unittest.mock import MagicMock
from flask import Flask
from src.adapters.drivers.http.controllers.user_controller import user_bp
from src.core.domain.application.services.user_service import UserService

class TestUserController(unittest.TestCase):
    def setUp(self):
        self.mock_user_service = MagicMock(spec=UserService)
        self.app = Flask(__name__)
        self.app.register_blueprint(user_bp(self.mock_user_service))
        self.client = self.app.test_client()

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



