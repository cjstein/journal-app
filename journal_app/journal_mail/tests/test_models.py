import pytest
from django.test import TestCase

from journal_app.users.tests.factories import UserFactory
from journal_app.journal.tests.factories import EntryFactory, ContactFactory
from journal_app.journal_mail.models import Mail


pytestmark = pytest.mark.django_db


class TestMailModel(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.contact = ContactFactory()
        self.entry = EntryFactory(user=self.user)
        self.entry.contact.add(self.contact)

    def test_mail_to_user(self):
        mail = Mail(
            user=self.user,
            subject='test',
            header='header',
            template_name='welcome_email'
        )
        mail.message()
        mail.refresh_from_db()
        # Test that the user email is used in the to field
        self.assertEqual(mail.to, self.user.email)
        # Test that the html message is converted to plain message
        self.assertIsNotNone(mail.plain_message)
        # Test that the date and time are not blank
        self.assertIsNotNone(mail.datetime)

    def test_mail_to_contact(self):
        mail = Mail(
            user=self.user,
            to=self.contact.email,
            subject='test',
            header='header',
            template_name='release_to_contact'
        )
        mail.message()
        mail.refresh_from_db()
        # Test that the contact email is use and not the user email
        self.assertEqual(mail.to, self.contact.email)
        self.assertNotEqual(mail.to, self.user.email)
