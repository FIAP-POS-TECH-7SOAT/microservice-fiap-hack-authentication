import unittest
from unittest.mock import MagicMock
from flask import Flask

from src.adapters.drivers.http.controllers.auth_controller import auth_bp
from src.core.domain.application.services.auth_service import AuthService

class TestAuthController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.mock_auth_service = MagicMock(spec=AuthService)
        self.app.register_blueprint(auth_bp(self.mock_auth_service))
        self.client = self.app.test_client()
        
    def test_check_auth(self):
        payload = {
            "user_email": "test_user@gmail.com",
            "password": "plain_password"
        }
        
        self.mock_auth_service.authenticate_user.return_value = "fake_token"
        
        response = self.client.post('/auth/check', json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("token", data)
        self.assertEqual(data["token"], "fake_token")
        
    def test_auth_verify(self):
        payload = {"token": "fake_token"}
        
        self.mock_auth_service.verify_token.return_value = {
            "sub":"fake_id",
            "user_email":"test_user@gmail.com",
            "phone":"+551112347896",
            "exp":"2022-12-31T00:00:00",
            "iat":"2021-12-31T00:00:00"
        }
        
        response = self.client.post('/auth/verify', json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("sub", data['payload'])
        self.assertIn("user_email", data['payload'])
        self.assertIn("phone", data['payload'])
        self.assertIn("exp", data['payload'])
        self.assertIn("iat", data['payload'])
        
        self.assertEqual(data['payload']["sub"], "fake_id")
        self.assertEqual(data['payload']["user_email"], "test_user@gmail.com")
        self.assertEqual(data['payload']["phone"], "+551112347896")
        self.assertEqual(data['payload']["exp"], "2022-12-31T00:00:00")
        self.assertEqual(data['payload']["iat"], "2021-12-31T00:00:00")
