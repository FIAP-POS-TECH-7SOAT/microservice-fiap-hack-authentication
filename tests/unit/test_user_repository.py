import unittest
from unittest.mock import MagicMock
from src.adapters.drivens.infra.repositories.user_repository import UserRepository
from src.core.domain.models.user_model import User

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.mock_session = MagicMock()
        self.mock_db.session = self.mock_session
        self.user_repository = UserRepository()
        self.user_repository.db = self.mock_db

    def test_save_user_success(self):
        user = User(
            user_email = "test_user@gmail.com",
            password = "hashed_password",
            phone = "+551112347896"
        )
        self.user_repository.save_user(user)
        self.mock_session.add.assert_called_once_with(user)
        self.mock_session.commit.assert_called_once()

    def test_get_user_success(self):
        mock_user = User(
            user_email="test_user@gmail.com",
            password="hashed_password",
            phone="+551112347896"
        )

        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_user
        User.query = MagicMock(return_value=mock_query)

        with unittest.mock.patch("src.core.domain.models.user_model.User.query", new=mock_query):
            result = self.user_repository.get_user("test_user@gmail.com")
            mock_query.filter_by.assert_called_once_with(user_email="test_user@gmail.com")
            self.assertEqual(result, mock_user)

    def test_delete_user_success(self):
        mock_user = User(
            user_email="test_user@gmail.com",
            password="hashed_password",
            phone="+551112347896"
        )
        
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_user
        self.mock_session.query.return_value = mock_query
        
        self.user_repository.get_user = MagicMock(return_value=mock_user)

        self.user_repository.delete_user("test_user@gmail.com")

        self.assertFalse(mock_user.active)
        self.mock_session.commit.assert_called_once()