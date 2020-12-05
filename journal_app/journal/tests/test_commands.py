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
        self.contact = ContactFactory()
        self.user1 = self.entry1.user
        self.user2 = self.entry2.user

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

    def test_release_entrires(self):
        """
        Check initialization state of users
        """
        assert self.user1.release_entries is False
        assert self.entry1.released is False
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
        assert self.user2.release_entries is False
        assert self.entry2.released is False
