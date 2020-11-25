import pytest
from django.core.exceptions import PermissionDenied
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse

from journal_app.journal.tests.factories import EntryFactory
from journal_app.journal.views import (
    EntryCreateView,
    EntryDetailView,
    EntryListView,
    EntryUpdateView,
)

pytestmark = pytest.mark.django_db


class TestEntryViews(TestCase):
    def setUp(self):
        # Every test needs access to the request factory
        self.factory = RequestFactory()
        self.entry1 = EntryFactory()
        self.entry2 = EntryFactory()
        self.user = self.entry1.user
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_detail_view(self):
        request = self.factory.get(reverse('journal:entry_detail', kwargs={'pk': self.entry1.uuid}))
        request.user = self.entry1.user
        callable_obj = EntryDetailView.as_view()
        response = callable_obj(request, pk=self.entry1.uuid)
        self.assertEqual(response.status_code, 200, 'Entry Detail')

    def test_wrong_detail_view(self):
        request = self.factory.get(reverse('journal:entry_detail', kwargs={'pk': self.entry1.uuid}))
        request.user = self.entry2.user
        callable_obj = EntryDetailView.as_view()
        response = callable_obj(request, pk=self.entry2.uuid) # noqa F841
        self.assertTemplateNotUsed(r'journal/entry_detail.html')
        self.assertTemplateUsed(r'journal/entry_list.html')

    def test_wrong_update_view(self):
        request = self.factory.get(reverse('journal:entry_update', kwargs={'pk': self.entry1.uuid}))
        request.user = self.entry2.user
        callable_obj = EntryUpdateView.as_view()
        with self.assertRaises(PermissionDenied):
            callable_obj(request, pk=self.entry1.uuid)

    def test_list_view(self):
        request = self.factory.get(reverse('journal:entry_list'))
        request.user = self.entry1.user
        callable_obj = EntryListView.as_view()
        response = callable_obj(request)
        self.assertEqual(response.status_code, 200, "Entry List")

    def test_create_view(self):
        request = self.factory.get(reverse('journal:entry_create'))
        request.user = self.entry1.user
        response = EntryCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200, "Entry Create")

    def test_create_success_view(self):
        response = self.client.post(
            reverse('journal:entry_create'),
            data={'title': 'Test title', 'body': 'random body data'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Entry Create Success")
        assert len(response.context['messages']) > 0

    def test_update_success_view(self):
        response = self.client.post(
            reverse('journal:entry_update', kwargs={'pk': self.entry1.pk}),
            data={'title': 'Test title 2', 'body': 'random updated body data'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Entry Create Success")
        assert len(response.context['messages']) > 0

    def test_wrong_delete_view(self):
        request = self.factory.get(reverse('journal:entry_delete', kwargs={'pk': self.entry1.uuid}))
        request.user = self.entry2.user
        callable_obj = EntryUpdateView.as_view()
        with self.assertRaises(PermissionDenied):
            callable_obj(request, pk=self.entry1.uuid)

    def test_delete_view_success(self):
        response = self.client.get(
            reverse('journal:entry_delete', kwargs={'pk': self.entry1.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Entry Delete")
