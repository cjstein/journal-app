from io import StringIO

import pytest
from django.core.management import call_command
from django.test import TestCase

from journal_app.subscription.tests.factories import ActiveSubscriberFactory
from journal_app.journal.tests.factories import ContactFactory, EntryFactory
from journal_app.journal_mail.models import Mail
from journal_app.users.tests.test_views import REFERENCE_DATE

pytestmark = pytest.mark.django_db


class TestReleaseEntries(TestCase):
    # Tests the releasing of Entries
    def setUp(self):
        """
        Settings up two different users and testing release of one Users set of entries
        """
        self.subscribed_customer1 = ActiveSubscriberFactory()
        self.subscribed_customer2 = ActiveSubscriberFactory()
        self.user1 = self.subscribed_customer1.user
        self.user2 = self.subscribed_customer2.user
        self.user1.email_verified = True
        self.user2.email_verified = True
        self.user1.save()
        self.user2.save()
        self.entry1 = EntryFactory(user=self.user1)
        self.entry2 = EntryFactory(user=self.user2)
        self.contact1 = ContactFactory(user=self.user1)
        self.contact2 = ContactFactory(user=self.user1)

    def call_command(self, *args, **kwargs):
        """
        This calls the release entry command.
        """
        out = StringIO()
        call_command(
            'release_entries',
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def test_release_entries(self):
        # Test the release of entries of user1 and making sure the other users Entries aren't released
        # Assure the entries are originally not released
        assert self.user1.release_entries is False
        assert self.entry1.released is False
        # Assure there is no contacts assigned originally
        self.assertQuerysetEqual(self.entry1.contact.all(), [])
        # Add the contact to the entry and refresh that the user ties to it again
        self.entry1.contact.add(self.contact1)
        self.entry1.save()
        self.user1.refresh_from_db()
        # Assure the contact was correctly added to the entry
        self.assertQuerysetEqual(self.entry1.contact.all(), [str(self.contact1)], transform=str)
        self._test_release_entries()
        assert self.user1.release_entries is False
        assert self.entry1.released is False
        assert self.user2.release_entries is False
        assert self.entry2.released is False
        # Change the reference date so the user last_checkin is is long ago so the entries get relesed
        self.user1.last_checkin = REFERENCE_DATE
        self.user1.save()
        self.user1.refresh_from_db()
        # Run the command and check they were released correctly
        out = self.call_command() # noqa F841
        self.entry1.refresh_from_db()
        self.entry2.refresh_from_db()
        assert self.user1.release_entries is True
        assert self.entry1.released is True
        # Check that the emails went out correctly
        user_email = Mail.objects.filter(to=self.user1.email)
        self.assertEqual(user_email[0].to, self.user1.email)
        contact1_emails = Mail.objects.filter(to=self.contact1.email)
        contact2_emails = Mail.objects.filter(to=self.contact2.email)
        self.assertEqual(contact1_emails[0].to, self.contact1.email)
        self.assertQuerysetEqual(contact2_emails, [])
        self._test_release_entries()
        self.user1.refresh_from_db()
        self.entry1.refresh_from_db()
        self.entry2.refresh_from_db()
        user_email = Mail.objects.filter(to=self.user1.email)
        self.assertEqual(user_email[0].to, self.user1.email)
        contact1_emails = Mail.objects.filter(to=self.contact1.email)
        contact2_emails = Mail.objects.filter(to=self.contact2.email)
        self.assertEqual(contact1_emails[0].to, self.contact1.email)
        self.assertQuerysetEqual(contact2_emails, [])

    def _test_release_entries(self):
        # Assure the other user and entry originally aren't released
        assert self.user2.release_entries is False
        assert self.entry2.released is False
        # We are calling the command with the current date and time as the last_checkin
        # to make sure the entries aren't released by accident
        out = self.call_command()


# TODO check release of entries for users who don't have verified email
# TODO check release of entries for scheduled Entries
