from io import StringIO

import pytest
from django.core.management import call_command
from django.test import TestCase

from journal_app.journal.tests.factories import ContactFactory, EntryFactory
from journal_app.journal_mail.models import Mail
from journal_app.users.tests.test_views import REFERENCE_DATE

pytestmark = pytest.mark.django_db


class TestReleaseEntries(TestCase):

    def setUp(self):
        """
        Settings up two different users and testing release of one Users set of entries
        """
        self.entry1 = EntryFactory()
        self.entry2 = EntryFactory()

        self.user1 = self.entry1.user
        self.user2 = self.entry2.user

        self.contact1 = ContactFactory(user=self.user1)
        self.contact2 = ContactFactory(user=self.user1)

    def call_command(self, *args, **kwargs):
        """
        This calls the release entry command.  This command
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
        """
        Check initialization state of users
        """
        assert self.user1.release_entries is False
        assert self.entry1.released is False
        self.assertQuerysetEqual(self.entry1.contact.all(), [])
        self.entry1.contact.add(self.contact1)
        self.entry1.save()
        self.user1.refresh_from_db()
        self.assertQuerysetEqual(self.entry1.contact.all(), [str(self.contact1)], transform=str)
        assert self.user2.release_entries is False
        assert self.entry2.released is False
        out = self.call_command()
        assert self.user1.release_entries is False
        assert self.entry1.released is False
        assert self.user2.release_entries is False
        assert self.entry2.released is False
        self.user1.last_checkin = REFERENCE_DATE
        self.user1.save()
        self.user1.refresh_from_db()
        out = self.call_command() # noqa F841
        self.entry1.refresh_from_db()
        assert self.user1.release_entries is True
        assert self.entry1.released is True
        user_email = Mail.objects.filter(to=self.user1.email)
        self.assertEqual(user_email[0].to, self.user1.email)
        contact1_emails = Mail.objects.filter(to=self.contact1.email)
        contact2_emails = Mail.objects.filter(to=self.contact2.email)
        self.assertEqual(contact1_emails[0].to, self.contact1.email)
        self.assertEqual(contact2_emails, [])
        assert self.user2.release_entries is False
        assert self.entry2.released is False

