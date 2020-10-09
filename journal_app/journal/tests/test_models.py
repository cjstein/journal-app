import pytest
from .factories import EntryFactory, ContactFactory

pytestmark = pytest.mark.django_db


# Entry Tests


def test_entry_str():
    entry = EntryFactory()
    assert entry.__str__() == entry.title
    assert str(entry) == entry.title


def test_entry_repr():
    entry = EntryFactory()
    assert entry.__repr__() == f'Entry({entry.user}, {entry.created}, {entry.title})'
    assert repr(entry) == f'Entry({entry.user}, {entry.created}, {entry.title})'


def test_entry_get_absolute_url():
    entry = EntryFactory()
    url = entry.get_absolute_url()
    assert url == f'/journal/entry/{entry.uuid}/'


def test_entry_update():
    entry = EntryFactory()
    assert entry.modified is False
    entry.body = 'Changing the body of the entry for the test to see if it is modified'
    entry.save()
    assert entry.modified is True


# Contact Tests


def test_contact_str():
    contact = ContactFactory()
    assert contact.__str__() == contact.name
    assert str(contact) == contact.name


def test_contact_repr():
    contact = ContactFactory()
    assert contact.__repr__() == f'Contact({contact.user}, {contact.name})'
    assert repr(contact) == f'Contact({contact.user}, {contact.name})'


def test_contact_get_absolute_url():
    contact = ContactFactory()
    url = contact.get_absolute_url()
    assert url == f'/journal/contact/{contact.uuid}/'
