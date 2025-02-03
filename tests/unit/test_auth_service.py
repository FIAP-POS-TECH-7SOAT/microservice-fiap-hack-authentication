import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import base64
import bcrypt
from jose import jwt

from src.core.domain.application.services.auth_service import AuthService
from src.adapters.drivens.infra.repositories.user_repository import UserRepository
from src.adapters.drivens.infra.settings.env import ENV
from src.adapters.drivers.http.dtos.user_request_dto import UserRequest
from src.adapters.drivers.http.dtos.token_request_dto import TokenRequest

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.mock_user_repository = MagicMock(spec=UserRepository)
        
        self.mock_env = MagicMock(spec=ENV)
        private_key_pem = """-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCjl14zQa4dA7fV\nPSLGrFspoq6N3jpklBhC1DYQkTEP7HMSUiOzSYwHM3lXfdTeEiBVDlFhjQiZxUJj\npsB37TAlD6hkWERSNUae9k1El2ksuGz9MxjnTMgDLtc7Z+Z6M3c+OZCHBLe4Rl+r\nIvjn8Egiji3H3mDTCQ9OXQA1ObwjZI209lHK7SQIP64eG8G+dGkJLp2S7Xtivizx\nk9GffVYKtfC6VaTQtdeUOrKjq4BxZ2/6ROkcEtGaqA6EIJIZQxIPh+A6QjdGE1Uh\nDmj6FAWTDg6UnvzvlvsdrOsEA+e5x0+KjrDVHoVtNHV6iCfSP6GkLDuJAimSZHMq\nJA8x+h3DAgMBAAECggEAAPJQJ+/PdaKxEUgdbUmuOqgo/JzZO5n2+pSIO3acpI+H\n3y2MW/wC4/1tlMOOxilhxkrSX1TMEoeGEhjMDbp0fmbsmFnzsmDEqplFlFqbfGuE\nJhiNDC9M9ZK2Q/dm/9YNZY19fxar1YwvY04KQhUfgTQznQuMHBbq6saoPaEIkFEo\nA8KzPOMdqX5xTKeOEZ5VLMJgBZr3R9Ds8V3hrZFy05WH8XMJ2A7qTcf72CxkuVXH\nMIxwgDgHYMUCHZR6u4/4qSiDsKdKeG3frsqzu0ZZ3uA8EzU2DW3lNc80dR01jeuH\nw/JDMOXlW6elCe3aiH4qcWYqfNnQvyIRktO2etNH3QKBgQDZOhO+uVNI58RVVm3A\nIAGFs5sySrjHLZ8mc9Gq8gvKmQ/h21+mQORlx2DK18mtt5QxRDgxikFAzuyxBbTi\nJCuTUanVRf6v78PKVRUBNuYo5/Gd6S6yE6c1+I6NsGm7vcJ+D+ndJbcaCWfmbDlL\nMjS0V+E9AbiTEdBFgubm8TrsRwKBgQDAynoM6WnB8QVqNWzamENb0uwjg1wg22mC\nXjSRN8khi+mu3w+2/kJL1Pa/btl0GYsJAod3WzeWzXAQnjvOsNsNyvj1fJc/QniA\ncN4e8G3qC/o7tkv4ARaghXPz/78Opa3h36g96DsdYUXcQzNxRLWZCorptL2zRfu9\n+lG/HW+MpQKBgFZ2vYE+9x2f0xA8tLayhqiXUwDzqRTu3dhKZXxrl7Huttmpniro\nzYCNmcNjnQ0ec0gg5VUiuNJ5CtFzegpBZ27eJIGVuMiC4SXaM+Al3/sMR6oZNNMA\n65+Z7fQL8ioeYBoZb3btGjKs58RZ83ww4bWe/TJxSuyPPJ1Oe2YVQuTlAoGAeeVL\nqDBI0vwufUnMSqYtKLjC321l6cxw+KHRwOOxwwkwtoWI7R30EvhTDxTqXtLrqsWz\nm07MZgf8zDUQAY6m4iCsqqKdCr1fbW5vssY36Nyr2edYPzWI9fOLLgJM7djpiUAd\now7bmabwQeUneH2GCH62+C90Jg6grizAVQMqjZUCgYAVnhfjjxIXgNKZ9FauO523\n6L0Khs4ijPLByvKNkpvmuilL48C5QY5mcrmr5P9R20nlpeg0QK1/5+uMPjr7ygkN\nc8e4IOlKi44Q2nLC173na5ZDIHFbrqGQ1Ty7dj9yDSi5ikLOTvoJ2xY3t9h5DluH\n4regItjbFgBATs2Jx7pcLQ==\n-----END PRIVATE KEY-----\n"""
        base64_key_private = base64.b64encode(private_key_pem.encode()).decode()
        self.mock_env.PRIVATE_KEY = base64_key_private
        public_key_pem = """-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAo5deM0GuHQO31T0ixqxb\nKaKujd46ZJQYQtQ2EJExD+xzElIjs0mMBzN5V33U3hIgVQ5RYY0ImcVCY6bAd+0w\nJQ+oZFhEUjVGnvZNRJdpLLhs/TMY50zIAy7XO2fmejN3PjmQhwS3uEZfqyL45/BI\nIo4tx95g0wkPTl0ANTm8I2SNtPZRyu0kCD+uHhvBvnRpCS6dku17Yr4s8ZPRn31W\nCrXwulWk0LXXlDqyo6uAcWdv+kTpHBLRmqgOhCCSGUMSD4fgOkI3RhNVIQ5o+hQF\nkw4OlJ7875b7HazrBAPnucdPio6w1R6FbTR1eogn0j+hpCw7iQIpkmRzKiQPMfod\nwwIDAQAB\n-----END PUBLIC KEY-----\n"""
        base64_key_public = base64.b64encode(public_key_pem.encode()).decode('utf-8')
        self.mock_env.PUBLIC_KEY = base64_key_public
        self.mock_env.EXP_DATE = "7"
        
        self.auth_service = AuthService()
        self.auth_service.user_repository = self.mock_user_repository
        self.auth_service.settings = self.mock_env

    @patch("bcrypt.checkpw")
    def test_authenticate_user_success(self, mock_checkpw):
        mock_user = MagicMock()
        mock_user.id = "1"
        mock_user.user_email = "test_user@gmail.com"
        mock_user.phone = "+551112347896"
        mock_user.password = bcrypt.hashpw(b"hashed_password", bcrypt.gensalt()).decode()

        self.mock_user_repository.get_user.return_value = mock_user
        mock_checkpw.return_value = True

        user_request = UserRequest(user_email="test_user@gmail.com", password="hashed_password")

        token = self.auth_service.authenticate_user(user_request)

        self.assertIsNotNone(token)
        public_key = base64.b64decode(self.mock_env.PUBLIC_KEY).decode('utf-8')
        decoded_token = jwt.decode(token, public_key, algorithms=["RS256"])
        self.assertEqual(decoded_token["sub"], mock_user.id)
        self.assertEqual(decoded_token["user_email"], mock_user.user_email)
        self.assertEqual(decoded_token["phone"], mock_user.phone)

    @patch("bcrypt.checkpw")
    def test_authenticate_user_invalid_credentials(self, mock_checkpw):
        mock_user = MagicMock()
        mock_user.password = bcrypt.hashpw(b"hashed_password", bcrypt.gensalt()).decode()

        self.mock_user_repository.get_user.return_value = mock_user
        mock_checkpw.return_value = False

        user_request = UserRequest(user_email="test_user@gmail.com", password="wrong_pass")

        with self.assertRaises(ValueError) as context:
            self.auth_service.authenticate_user(user_request)

        self.assertEqual(str(context.exception), "Invalid password")

    def test_verify_token_success(self):
        payload = {
            "sub": "1",
            "user_email": "test_user@gmail.com",
            "phone": "+551112347896",
            "exp": (datetime.now() + timedelta(days=7)).timestamp(),
            "iat": datetime.now().timestamp(),
        }

        private_key = base64.b64decode(self.mock_env.PRIVATE_KEY).decode('utf-8')
        token = jwt.encode(payload, private_key, algorithm="RS256")

        token_request = TokenRequest(token=token)

        decoded_payload = self.auth_service.verify_token(token_request)

        self.assertEqual(decoded_payload["sub"], payload["sub"])
        self.assertEqual(decoded_payload["user_email"], payload["user_email"])
        self.assertEqual(decoded_payload["phone"], payload["phone"])

    def test_verify_token_invalid_token(self):
        invalid_token = "invalid_token"
        token_request = TokenRequest(token=invalid_token)

        with self.assertRaises(ValueError):
            self.auth_service.verify_token(token_request)