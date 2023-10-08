import unittest

from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import UserModel, UserDb
from src.repository.users import get_user_by_email, create_user


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email_found(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email="test@example.net", db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email="test@example.net", db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(username="Test", email="test@example.net", password="123456789")
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)


if __name__ == '__main__':
    unittest.main()
