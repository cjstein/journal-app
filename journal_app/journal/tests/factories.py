import pytest
from factory import Faker, fuzzy, SubFactory
from factory.django import DjangoModelFactory
from journal_app.users.tests.factories import UserFactory
from journal_app.journal.models import Entry, Contact


@pytest.fixture
def entry():
    return EntryFactory()


@pytest.fixture
def contact():
    return ContactFactory()


class EntryFactory(DjangoModelFactory):

    title = fuzzy.FuzzyText()
    body = fuzzy.FuzzyText()
    released = fuzzy.FuzzyChoice([True, False])
    public = fuzzy.FuzzyChoice([True, False])
    user = SubFactory(UserFactory)

    class Meta:
        model = Entry


class ContactFactory(DjangoModelFactory):

    name = fuzzy.FuzzyText()
    user = SubFactory(UserFactory)
    email = Faker('email')

    class Meta:
        model = Contact
