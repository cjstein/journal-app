import pytest
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse

from journal_app.journal.tests.factories import EntryFactory, ContactFactory
from journal_app.users.tests.factories import UserFactory
from journal_app.journal.views import (
    EntryCreateView,
    EntryDetailView,
    EntryListView,
    EntryUpdateView,
)
from journal_app.users.tests.test_views import REFERENCE_DATE

pytestmark = pytest.mark.django_db


class TestEntryViews(TestCase):
    # Test each of the views for entries
    def setUp(self):
        # Every test needs access to the request factory
        self.factory = RequestFactory()
        self.entry1 = EntryFactory()
        self.entry2 = EntryFactory()
        self.user = self.entry1.user
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_detail_view(self):
        # Tests the view of someone who owns an Entry
        request = self.factory.get(reverse('journal:entry_detail', kwargs={'pk': self.entry1.uuid}))
        request.user = self.entry1.user
        callable_obj = EntryDetailView.as_view()
        response = callable_obj(request, pk=self.entry1.uuid)
        self.assertEqual(response.status_code, 200, 'Entry Detail')

    def test_wrong_detail_view(self):
        # Tests if someone tries to see a view they don't own
        self.client = Client()
        self.client.force_login(user=self.entry1.user)
        response = self.client.get(
            reverse('journal:entry_detail', kwargs={'pk': self.entry2.uuid}),
            follow=True,
        )
        self.assertEqual(response.status_code, 403, "Redirects correctly")
        self.assertTemplateNotUsed(r'journal/entry_detail.html')
        self.assertTemplateUsed(r'journal/entry_list.html')

    def test_wrong_update_view(self):
        # Tests someone accessing an update view they don't own
        self.client = Client()
        self.client.force_login(user=self.entry1.user)
        response = self.client.get(
            reverse('journal:entry_update', kwargs={'pk': self.entry2.uuid}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Redirects correctly")
        self.assertTemplateNotUsed(r'journal/entry_update.html')
        self.assertTemplateUsed(r'journal/entry_list.html')

    def test_list_view(self):
        # Tests that the list view is routed correctly
        request = self.factory.get(reverse('journal:entry_list'))
        request.user = self.entry1.user
        callable_obj = EntryListView.as_view()
        response = callable_obj(request)
        self.assertEqual(response.status_code, 200, "Entry List")

    def test_create_view(self):
        # Tests that the Create view is routed correctly
        request = self.factory.get(reverse('journal:entry_create'))
        request.user = self.entry1.user
        response = EntryCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200, "Entry Create")

    def test_create_success_view(self):
        # Tests that the create view is successful and redirects correctly and has a success message
        response = self.client.post(
            reverse('journal:entry_create'),
            data={'title': 'Test title', 'body': 'random body data'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Entry Create Success")
        assert len(response.context['messages']) > 0

    def test_update_success_view(self):
        # Tests that an update is routed correctly and has a success message
        response = self.client.post(
            reverse('journal:entry_update', kwargs={'pk': self.entry1.pk}),
            data={'title': 'Test title 2', 'body': 'random updated body data'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Entry Create Success")
        assert len(response.context['messages']) > 0

    def test_wrong_delete_view(self):
        # Tests that someone can't delete another persons Entry
        self.client.force_login(user=self.entry2.user)
        response = self.client.get(
            reverse('journal:entry_delete', kwargs={'pk': self.entry1.uuid}),
            follow=True
        )
        self.assertEqual(response.status_code, 403, "Wrong Entry Delete Success")

    def test_delete_view_success(self):
        # Tests that someone can delete successfully
        response = self.client.get(
            reverse('journal:entry_delete', kwargs={'pk': self.entry1.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Entry Delete")

    # TODO create scheduled test view


class TestContactViews(TestCase):
    # These tests are for contact views
    def setUp(self):
        # Every test needs access to the request factory
        self.user = UserFactory(last_checkin=REFERENCE_DATE)
        self.entry_with_contact = EntryFactory(user=self.user)
        self.entry_no_contact = EntryFactory(user=self.user)
        self.contact = ContactFactory(user=self.user)
        self.entry_with_contact.contact.add(self.contact)
        self.entry_with_contact.save()
        self.contact.save()
        self.user.save()
        call_command('release_entries')
        self.user.refresh_from_db()
        self.entry_with_contact.refresh_from_db()
        self.entry_no_contact.refresh_from_db()
        self.contact.refresh_from_db()
        self.client = Client()

    def test_entries_released_list(self):
        # Tests that the contact list view is routed correctly
        response = self.client.get(
            reverse('journal:released_entries', kwargs={'contact': self.contact.uuid}),
        )

        self.assertEqual(response.status_code, 200, "Released Entries List Page")
        self.assertTemplateUsed(response, 'journal/entry_list.html')

    def test_entries_released_detail(self):
        # Tests that a contact can visit an Entry detail page after being released
        self.client = Client()
        response = self.client.get(
            reverse('journal:released_entry_detail',
                    kwargs={'contact': self.contact.uuid, 'pk': self.entry_with_contact.pk}
                    ),
        )
        self.assertEqual(response.status_code, 200, "Released Entries Detail Page")
        self.assertTemplateUsed(response, 'journal/entry_detail.html')
