import pytest
from django.urls import reverse
from django.test import RequestFactory, TestCase
from journal_app.journal.tests.factories import EntryFactory, ContactFactory
from journal_app.journal.views import (
    EntryCreateView, EntryUpdateView, EntryDetailView, EntryListView,
    ContactCreateView, ContactUpdateView, ContactDetailView, ContactListView,
)

pytestmark = pytest.mark.django_db


class TestEntryViews(TestCase):
    def setUp(self):
        # Every test needs access to the request factory
        self.factory = RequestFactory()
        self.entry1 = EntryFactory()
        self.entry2 = EntryFactory()

    def test_detail_view(self):
        request = self.factory.get(reverse('journal:entry_detail', kwargs={'pk': self.entry1.uuid}))
        request.user = self.entry1.user
        callable_obj = EntryDetailView.as_view()
        response = callable_obj(request, pk=self.entry1.uuid)
        self.assertEqual(response.status_code, 200, 'Entry Detail')

    def test_wrong_detail_view(self):
        request = self.factory.get(reverse('journal:entry_detail', kwargs={'pk': self.entry1.uuid}))
        callable_obj = EntryDetailView.as_view()
        response = callable_obj(request, pk=self.entry2.uuid)
        self.assertEqual(response.status_code, 403, '403')

    def test_list_view(self):
        request = self.factory.get(reverse('journal:entry_list'))
        request.user = self.entry1.user
        callable_obj = EntryListView.as_view()
        response = callable_obj(request)
        self.assertEqual(response.status_code, 200, "Entry List")

    def test_create_view(self):
        request = self.factory.get(reverse('journal:entry_create'))
        request.user = self.entry1.user
        callable_obj = EntryCreateView.as_view()
        response = callable_obj(request)
        self.assertEqual(response.status_code, 200, "Entry Create")
