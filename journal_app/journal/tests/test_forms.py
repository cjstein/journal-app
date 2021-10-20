from django.test import TestCase

import pytest

from journal_app.journal.forms import ContactForm, EntryForm
from journal_app.journal.tests.factories import ContactFactory
from journal_app.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def _create_form(values):
    keys = 'name email phone'.split()
    data = dict(zip(keys, values))
    return ContactForm(data=data)


def test_contact_form_validation_requires_name():
    values = ('', 'cj@journal.com', '2223334444')
    form = _create_form(values)
    assert not form.is_valid()
    assert form.errors == {'name': ['This field is required.']}


def test_contact_form_validation_bad_number():
    values = ('Bad Number', 'cj@journal.com', '222-333-4444')
    form = _create_form(values)
    assert not form.is_valid()
    assert form.errors == {'phone': ['Phone number must be 10 digits long with no spaces, dashes, or parenthesis']}


def test_contact_form_validation_needs_at_least_one_contact_field():
    values = ('cj', '', '')
    form = _create_form(values)
    assert not form.is_valid()
    assert form.errors == {
        'email': ['At least one of Email or Phone needs to filled'],
        'phone': ['At least one of Email or Phone needs to filled'],
    }


@pytest.mark.parametrize("email, phone", [
    ('cj@journal.com', ''),
    ('', '2223334444'),
])
def test_contact_form_validation_passes_with_one_contact_field(
        email, phone):
    values = ('cj', email, phone)
    form = _create_form(values)
    assert form.is_valid()
    assert form.errors == {}


class TestEntryForm(TestCase):

    def test_entry_form_contact_list(self):
        user1 = UserFactory()
        user2 = UserFactory()
        for i in range(10):
            ContactFactory(user=user1)
            ContactFactory(user=user2)
        user1_contacts = [str(i) for i in user1.contact_set.all()]
        user2_contacts = [str(i) for i in user2.contact_set.all()]
        entry_form1 = EntryForm(user=user1)
        entry_form2 = EntryForm(user=user2)
        self.assertQuerysetEqual(entry_form1.fields['contact'].queryset, user1_contacts, transform=str)
        self.assertQuerysetEqual(entry_form2.fields['contact'].queryset, user2_contacts, transform=str)
