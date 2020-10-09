import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse
from django.test import RequestFactory, TestCase

from journal_app.users.models import User

from .factories import EntryFactory
from journal_app.journal.views import (
    EntryCreateView, EntryUpdateView, EntryDetailView, EntryListView,
    ContactCreateView, ContactUpdateView, ContactDetailView, ContactListView,
)


@pytest.mark.django_db
class TestEntryViews(TestCase):
    def setUp(self):
        # Every test needs access to the request factory
        self.factory = RequestFactory()
        self.user = User()
        self.anon_user = AnonymousUser()
        self.entry = EntryFactory()

    def test_detail_view(self):
        request = self.factory.get(reverse('journal:entry_detail', kwargs={'pk': self.entry.uuid}))
        request.user = self.user
        callable_obj = EntryDetailView.as_view()
        response = callable_obj(request, pk=self.entry.uuid)
        self.assertEquals(response.status_code, 200, 'Entry Detail')

    def test_list_view(self):
        request = self.factory.get(reverse('journal:entry_list'))
        request.user = self.user
        callable_obj = EntryListView.as_view()
        response = callable_obj(request)
        self.assertEquals(response.status_code, 200, "Entry List")

    def test_create_view(self):
        request = self.factory.get(reverse('journal:entry_create'))
        request.user = self.user
        callable_obj = EntryCreateView.as_view()
        response = callable_obj(request)
        self.assertEquals(response.status_code, 200, "Entry Create")
