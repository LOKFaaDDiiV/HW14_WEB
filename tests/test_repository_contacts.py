import unittest

from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from datetime import datetime, date

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate
from src.repository.contacts import (find_contacts, get_contacts, get_contact, get_birthdays, create_contact,
                                     update_contact, remove_contact)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(firstname="example", lastname="test", phone_number="0123456789",
                            email="test@example.net", date_of_birth=datetime.now().date(), relationships="test")
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.firstname, body.firstname)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.date_of_birth, body.date_of_birth)
        self.assertEqual(result.relationships, body.relationships)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactUpdate(firstname="Example", lastname="Test", phone_number="0123456789", email="test@example.net",
                             date_of_birth=datetime.now().date(), relationships="test")
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactUpdate(firstname="Example", lastname="Test", phone_number="0123456789", email="test@example.net",
                             date_of_birth=datetime.now().date(), relationships="test")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_birthdays(self):
        contact = Contact(firstname="test", lastname="test-name", phone_number="test-phone-number", email="test-email",
                          date_of_birth=date(2000, 10, 13), relationships='test')
        self.session.query().filter().all.return_value = [contact]
        result = await get_birthdays(user=self.user, db=self.session)
        self.assertEqual(result, [contact])

    async def test_find_contact_by_firstname_found(self):
        contact = Contact()
        self.session.query().filter().filter().all.return_value = contact
        result = await find_contacts(user=self.user, db=self.session, firstname="example")
        self.assertEqual(result, contact)

    async def test_find_contact_by_lastname_found(self):
        contact = Contact()
        self.session.query().filter().filter().all.return_value = contact
        result = await find_contacts(user=self.user, db=self.session, lastname="test")
        self.assertEqual(result, contact)

    async def test_find_contact_by_email_found(self):
        contact = Contact()
        self.session.query().filter().filter().all.return_value = contact
        result = await find_contacts(user=self.user, db=self.session, email="test@example.net")
        self.assertEqual(result, contact)

    async def test_find_contact_not_found(self):
        contact = Contact()
        self.session.query().filter().filter().all.return_value = None
        result = await find_contacts(user=self.user, db=self.session, firstname="Example")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
