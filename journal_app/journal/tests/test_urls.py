import pytest
from django.urls import resolve, reverse

from .factories import contact, entry  # noqa F401

pytestmark = pytest.mark.django_db


def test_entry_list_reverse():
    assert reverse('journal:entry_list') == '/journal/'


def test_entry_list_resolve():
    assert resolve('/journal/').view_name == 'journal:entry_list'


@pytest.mark.django_db
def test_entry_detail_reverse(entry): # noqa F811
    url = reverse('journal:entry_detail', kwargs={'pk': entry.uuid})
    assert url == f'/journal/entry/{entry.uuid}/'


@pytest.mark.django_db
def test_entry_detail_resolve(entry):  # noqa F811
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


def test_contact_add_reverse():
    assert reverse('journal:contact_create') == '/journal/contact/new/'


def test_contact_add_resolve():
    assert resolve('/journal/contact/new/').view_name == 'journal:contact_create'
