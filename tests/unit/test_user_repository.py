import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.exc import SQLAlchemyError

from src.adapters.drivens.infra.repositories.user_repository import UserRepository
from src.core.domain.models.user_model import User
from server import app

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
            
    def test_get_user_failure(self):
        with app.app_context():
            with patch("src.core.domain.models.user_model.User.query") as mock_query:
                mock_query.filter_by.return_value.first.side_effect = SQLAlchemyError("Database error")

                with self.assertRaises(SQLAlchemyError):
                    self.user_repository.get_user("test_user@gmail.com")

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
        
    def test_update_password_success(self):
        mock_user = User(
            user_email="test_user@gmail.com",
            password="old_password",
            phone="+551112347896"
        )
        self.user_repository.get_user = MagicMock(return_value=mock_user)
        self.user_repository.update_password("test_user@gmail.com", "new_hashed_password")
        self.assertEqual(mock_user.password, "new_hashed_password")
        self.mock_session.commit.assert_called_once()

    def test_update_password_user_not_found(self):
        self.user_repository.get_user = MagicMock(return_value=None)
        self.user_repository.update_password("nonexistent@gmail.com", "new_password")
        self.mock_session.commit.assert_not_called()

    def test_update_verification_success(self):
        mock_user = User(
            user_email="test_user@gmail.com",
            password="hashed_password",
            phone="+551112347896",
            email_verified=False
        )
        self.user_repository.update_verification(mock_user)
        self.assertTrue(mock_user.email_verified)
        self.mock_session.commit.assert_called_once()

    def test_update_verification_failure(self):
        mock_user = User(
            user_email="test_user@gmail.com",
            password="hashed_password",
            phone="+551112347896",
            email_verified=False
        )
        self.mock_session.commit.side_effect = SQLAlchemyError("Database error")
        with self.assertRaises(SQLAlchemyError):
            self.user_repository.update_verification(mock_user)
        self.mock_session.rollback.assert_called_once()