import unittest
from unittest.mock import MagicMock, patch
from src.adapters.drivers.http.dtos.create_user_request_dto import CreateUserRequest
from src.core.domain.application.services.user_service import UserService
from src.adapters.drivens.infra.repositories.user_repository import UserRepository
from src.core.domain.models.user_model import User

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.mock_user_repository = MagicMock(spec=UserRepository)
        self.user_service = UserService()
        self.user_service.user_repository = self.mock_user_repository

    def test_register_user_success(self):
        user_request = CreateUserRequest(
            user_email="test_user@gmail.com",
            password="plain_password",
            phone="+551112347896"
        )
        
        self.mock_user_repository.get_user.return_value = None
        self.mock_user_repository.save_user.return_value = None

        with patch("bcrypt.hashpw") as mock_hashpw:
            mock_hashpw.return_value = b"hashed_password"
            result = self.user_service.register_user(user_request)

            self.assertTrue(result)
            self.mock_user_repository.save_user.assert_called_once()
            saved_user = self.mock_user_repository.save_user.call_args[0][0]
            self.assertEqual(saved_user.password, "hashed_password")

    def test_register_user_already_exists(self):
        user_request = CreateUserRequest(
            user_email="test_user@gmail.com",
            password="plain_password",
            phone="+551112347896"
        )
        
        existing_user = User(
            user_email="test_user@gmail.com",
            password="hashed_password",
            phone="+551112347896"
        )
        self.mock_user_repository.get_user.return_value = existing_user

        with self.assertRaises(ValueError) as context:
            self.user_service.register_user(user_request)

        self.assertEqual(str(context.exception), "Invalid data: User already exists")
        self.mock_user_repository.save_user.assert_not_called()

    def test_delete_user_success(self):
        user = User(
            user_email="test_user@gmail.com",
            password="hashed_password",
            phone="+551112347896"
        )
        self.mock_user_repository.get_user.return_value = user

        result = self.user_service.delete_user("test_user@gmail.com")

        self.assertEqual(result, f"User {user.user_email} deleted!")
        self.mock_user_repository.get_user.assert_called_once_with("test_user@gmail.com")
        self.mock_user_repository.delete_user.assert_called_once_with("test_user@gmail.com")
        
    def test_delete_user_not_found(self):
        self.mock_user_repository.get_user.return_value = None

        with self.assertRaises(ValueError) as context:
            self.user_service.delete_user("non_existent_user@gmail.com")

        self.assertEqual(str(context.exception), "User does not exist")
        self.mock_user_repository.delete_user.assert_not_called()

    def test_register_user_save_failure(self):
        user_request = CreateUserRequest(
            user_email="test_user@gmail.com",
            password="plain_password",
            phone="+551112347896"
        )
        
        self.mock_user_repository.get_user.return_value = None
        self.mock_user_repository.save_user.side_effect = Exception("Database error")

        with self.assertRaises(ValueError) as context:
            self.user_service.register_user(user_request)

        self.assertIn("Invalid data", str(context.exception))
        self.mock_user_repository.save_user.assert_called_once()

    def test_delete_user_repository_failure(self):
        existing_user = User(
            user_email="test_user@gmail.com",
            password="hashed_password",
            phone="+551112347896"
        )
        self.mock_user_repository.get_user.return_value = existing_user
        self.mock_user_repository.delete_user.side_effect = Exception("Database error")

        with self.assertRaises(Exception):
            self.user_service.delete_user("test_user@gmail.com")

        self.mock_user_repository.delete_user.assert_called_once_with("test_user@gmail.com")