from django.contrib.sites.models import Site

import pytest

from journal_app.journal.tests.factories import ContactFactory, EntryFactory

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
    domain = Site.objects.get_current().domain
    assert url == f'{domain}/journal/entry/{entry.uuid}/'


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
    domain = Site.objects.get_current().domain
    assert url == f'{domain}/journal/contact/{contact.uuid}/entries/'
