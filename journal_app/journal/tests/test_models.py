import pytest
from time import sleep
from journal_app.journal.tests.factories import EntryFactory, ContactFactory
from journal_app.journal.models import Entry, Contact
from journal_app.users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_entry_str():
    entry = EntryFactory()
    assert str(entry) == entry.title


def test_entry_repr():
    entry = EntryFactory()
    assert repr(entry) == f'Entry({entry.user}, {entry.title})'


def test_entry_get_absolute_url():
    entry = EntryFactory()
    url = entry.get_absolute_url()
    assert url == f'/journal/entry/{entry.uuid}/'


def test_entry_update():
    entry = EntryFactory()
    assert entry.created == entry.updated
    assert entry.modified is False
    """
    below assert fails
    -> return self.updated != self.created
    (Pdb) self.updated
    datetime.datetime(2020, 10, 15, 11, 5, 22, 722688, tzinfo=<UTC>)
    (Pdb) self.created
    datetime.datetime(2020, 10, 15, 11, 5, 22, 722668, tzinfo=<UTC>)
    """
    # assert entry.modified is False
    entry.body = 'Changing the body of the entry for the test to see if it is modified'
    sleep(1)
    entry.save()
    assert entry.created != entry.updated
    assert entry.modified is True


# Contact Tests


def test_contact_str():
    contact = ContactFactory()
    assert str(contact) == contact.name


def test_contact_repr():
    contact = ContactFactory()
    assert repr(contact) == f'Contact({contact.user}, {contact.name})'


def test_contact_get_absolute_url():
    contact = ContactFactory()
    url = contact.get_absolute_url()
    assert url == f'/journal/contact/{contact.uuid}/update/'
