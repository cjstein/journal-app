import pytest

from django.urls import reverse, resolve
from .factories import entry, contact

pytestmark = pytest.mark.django_db


def test_entry_list_reverse():
    assert reverse('journal:entry_list') == '/journal/'


def test_entry_list_resolve():
    assert resolve('/journal/').view_name == 'journal:entry_list'


@pytest.mark.django_db
def test_entry_detail_reverse(entry):
    url = reverse('journal:entry_detail', kwargs={'pk': entry.uuid})
    assert url == f'/journal/entry/{entry.uuid}/'


@pytest.mark.django_db
def test_entry_detail_resolve(entry):
    url = f'/journal/entry/{entry.uuid}/'
    assert resolve(url).view_name == 'journal:entry_detail'


def test_entry_add_reverse():
    assert reverse('journal:entry_create') == '/journal/entry/new/'


def test_entry_add_resolve():
    assert resolve('/journal/entry/new/').view_name == 'journal:entry_create'


# Test contact urls


def test_contact_list_reverse():
    assert reverse('journal:contact_list') == '/journal/contacts/'


def test_contact_list_resolve():
    assert resolve('/journal/contacts/').view_name == 'journal:contact_list'


@pytest.mark.django_db
def test_contact_detail_reverse(contact):
    url = reverse('journal:contact_detail', kwargs={'pk': contact.uuid})
    assert url == f'/journal/contact/{contact.uuid}/'


@pytest.mark.django_db
def test_contact_detail_resolve(contact):
    url = f'/journal/contact/{contact.uuid}/'
    assert resolve(url).view_name == 'journal:contact_detail'


def test_contact_add_reverse():
    assert reverse('journal:contact_create') == '/journal/contact/new/'


def test_contact_add_resolve():
    assert resolve('/journal/contact/new/').view_name == 'journal:contact_create'
