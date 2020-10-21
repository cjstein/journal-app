import pytest
from io import StringIO
from random import choice

from django.core.management import call_command
from django.test import TestCase

from journal_app.journal.models import Entry, Contact
from journal_app.users.tests.test_views import REFERENCE_DATE
from journal_app.journal.tests.factories import EntryFactory, ContactFactory
from journal_app.users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


class TestReleaseEntries(TestCase):

    def setUp(self):
        self.entry1 = EntryFactory()
        self.entry2 = EntryFactory()
        self.contact = ContactFactory()
        self.entries = [EntryFactory() for _ in range(100)]
        self.choices = []

    def call_command(self, *args, **kwargs):
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
        assert self.entry1.user.release_entries is False
        assert self.entry1.released is False
        assert self.entry2.user.release_entries is False
        assert self.entry2.released is False
        out = self.call_command()
        assert self.entry1.user.release_entries is False
        assert self.entry1.released is False
        assert self.entry2.user.release_entries is False
        assert self.entry2.released is False
        self.entry1.user.last_checkin = REFERENCE_DATE
        self.entry1.user.save()
        self.entry1.user.refresh_from_db()
        out = self.call_command()
        self.entry1.refresh_from_db()
        assert self.entry1.user.release_entries is True
        assert self.entry1.released is True
        assert self.entry2.user.release_entries is False
        assert self.entry2.released is False

    def test_random_entries(self):
        for entry in self.entries:
            assert entry.released is False
            assert entry.user.release_entries is False
        out = self.call_command()
        for entry in self.entries:
            assert entry.released is False
            assert entry.user.release_entries is False
            selection = choice([True, False])
            self.choices.append(selection)
            if selection:
                entry.user.last_checkin = REFERENCE_DATE
                entry.user.save()
        out = self.call_command()
        for selection, entry in zip(self.choices, self.entries):
            entry.refresh_from_db()
            if selection:
                assert entry.user.release_entries is True
                assert entry.released is True
            else:
                assert entry.user.release_entries is False
                assert entry.released is False
