import pytest

from journal_app.journal.forms import ContactForm


def _create_form(values):
    keys = 'name email phone'.split()
    data = dict(zip(keys, values))
    return ContactForm(data=data)


def test_contact_form_validation_requires_name():
    values = ('', 'cj@journal.com', '222-333-4444')
    form = _create_form(values)
    assert not form.is_valid()
    assert form.errors == {'name': ['This field is required.']}


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
    ('', '222-333-4444'),
])
def test_contact_form_validation_passes_with_one_contact_field(
        email, phone):
    values = ('cj', email, phone)
    form = _create_form(values)
    assert form.is_valid()
    assert form.errors == {}
