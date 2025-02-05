import unittest
from unittest.mock import MagicMock, patch
from flask import Flask

from src.adapters.drivens.infra.settings.env import ENV
from src.adapters.drivers.http.controllers.password_controller import password_recovery_bp
from src.core.domain.application.services.user_service import UserService

class TestPasswordController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.mock_user_service = MagicMock(spec=UserService)
        env = ENV()
        self.app.register_blueprint(password_recovery_bp(self.mock_user_service, env.SALT_KEY))
        self.client = self.app.test_client()
        
    
    def test_recover_password_success(self):
        payload = {
            "user_email": "test_user@gmail.com"
        }
        
        self.mock_user_service.get_user_by_email.return_value = MagicMock(user_email="test_user@gmail.com")
        
        response = self.client.post('/password/recover', json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Recovery email sent")
        
    def test_recover_password_user_not_found(self):
        payload = {
            "user_email": "test_user@gmail.com"
        }

        self.mock_user_service.get_user_by_email.return_value = None

        response = self.client.post('/password/recover', json=payload)

        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json["error"])
        
    def test_recover_password_token_failure(self):
        payload = {
            "user_email": "test_user@gmail.com"
        }

        self.mock_user_service.get_user_by_email.return_value = MagicMock(user_email="test_user@gmail.com")

        with patch("itsdangerous.URLSafeTimedSerializer.dumps", side_effect=Exception("Token error")):
            response = self.client.post('/password/recover', json=payload)

        data = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)
        self.assertIn("Unable to process request", data['error'])
        
    def test_recover_password_email_failure(self):
        payload = {
            "user_email": "test_user@gmail.com"
        }

        self.mock_user_service.get_user_by_email.return_value = MagicMock(user_email="test_user@gmail.com")

        with patch("src.core.domain.application.services.email_service.MailSend.send_email", side_effect=Exception("Email error")):
            response = self.client.post('/password/recover', json=payload)
        
        data = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)
        self.assertIn("Unable to process request", data['error'])
        
    def test_reset_password_success(self):
        payload = {
            "new_password": "new_password_test"
        }
        
        self.mock_user_service.get_user_by_email.return_value = MagicMock(user_email="test_user@gmail.com")
        self.mock_user_service.update_password.return_value = True
        
        with patch("itsdangerous.URLSafeTimedSerializer.loads"):
            response = self.client.post('/password/reset/<token>', json=payload)
        
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)
        self.assertIn("Password reset successful", data['message'])
        
    
    def test_reset_password_token_failure(self):
        payload = {
            "new_password": "new_password_test"
        }

        with patch("itsdangerous.URLSafeTimedSerializer.loads", side_effect=Exception("Invalid or expired token")):
            response = self.client.post('/password/reset/<token>', json=payload)

        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertIn("Invalid or expired token", data['error'])
        
    def test_reset_password_user_not_found(self):
        payload = {
            "new_password": "new_password_test"
        }
        
        self.mock_user_service.get_user_by_email.return_value = None

        with patch("itsdangerous.URLSafeTimedSerializer.loads"):
            response = self.client.post('/password/reset/<token>', json=payload)

        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json["error"])
        
    def test_reset_password_update_password_failure(self):
        payload = {
            "new_password": "new_password_test"
        }
        
        self.mock_user_service.get_user_by_email.return_value = MagicMock(user_email="test_user@gmail.com")
        self.mock_user_service.update_password.return_value = False
        
        with patch("itsdangerous.URLSafeTimedSerializer.loads"):
            response = self.client.post('/password/reset/<token>', json=payload)
        
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)
        self.assertIn("Password not reseted", data['error'])