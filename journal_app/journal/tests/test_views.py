from django.core.management import call_command
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse_lazy

import pytest

from journal_app.journal.tests.factories import ContactFactory, EntryFactory
from journal_app.journal.views import (EntryCreateView, EntryDetailView,
                                       EntryListView)
from journal_app.subscription.tests.factories import create_active_subscriber, create_trial_subscriber
from journal_app.users.tests.factories import UserFactory
from journal_app.users.tests.test_views import REFERENCE_DATE

pytestmark = pytest.mark.django_db


class TestEntryViews(TestCase):
    # Test each of the views for entries
    def setUp(self):
        # Every test needs access to the request factory
        self.user = UserFactory()
        self.factory = RequestFactory()
        self.subscribed_customer = create_active_subscriber(self.user)
        self.user.email_verified = True
        self.user.save()
        self.user.refresh_from_db()
        self.entry1 = EntryFactory(user=self.user)
        self.entry2 = EntryFactory(user=self.user)
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_detail_view(self):
        # Tests the view of someone who owns an Entry
        request = self.factory.get(reverse_lazy('journal:entry_detail', kwargs={'pk': self.entry1.uuid}))
        request.user = self.entry1.user
        callable_obj = EntryDetailView.as_view()
        response = callable_obj(request, pk=self.entry1.uuid)
        self.assertEqual(response.status_code, 200, 'Entry Detail')

    def test_wrong_detail_view(self):
        # Tests if someone tries to see a view they don't own
        response = self.client.get(
            reverse_lazy('journal:entry_detail', kwargs={'pk': self.entry2.uuid}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Redirects correctly")
        self.assertTemplateNotUsed(r'journal/entry_detail.html')
        self.assertTemplateUsed(r'journal/entry_list.html')

    def test_wrong_update_view(self):
        # Tests someone accessing an update view they don't own
        response = self.client.get(
            reverse_lazy('journal:entry_update', kwargs={'pk': self.entry2.uuid}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Redirects correctly")
        self.assertTemplateNotUsed(r'journal/entry_update.html')
        self.assertTemplateUsed(r'journal/entry_list.html')

    def test_list_view(self):
        # Tests that the list view is routed correctly
        response = self.client.get(reverse_lazy('journal:entry_list'))
        self.assertEqual(response.status_code, 200, "Entry List")

    def test_create_view(self):
        # Tests that the Create view is routed correctly
        response = self.client.get(reverse_lazy('journal:entry_create'))
        self.assertEqual(response.status_code, 200, "Entry Create")

    def test_create_success_view(self):
        # Tests that the create view is successful and redirects correctly and has a success message
        self.assertEqual(self.user.customer.status, 'active')
        response = self.client.post(
            reverse_lazy('journal:entry_create'),
            data={
                'title': 'Test title',
                'body': 'random body data',
                'public': False,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Entry Create Success")
        self.assertRedirects(response, reverse_lazy('journal:entry_detail', kwargs={'pk': response.context['entry'].uuid}))
        assert len(response.context['messages']) > 0

    def test_update_success_view(self):
        # Tests that an update is routed correctly and has a success message
        response = self.client.post(
            reverse_lazy('journal:entry_update', kwargs={'pk': self.entry1.pk}),
            data={
                'title': 'Test title 2',
                'body': 'random updated body data',
                'public': False,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Entry Create Success")
        self.assertRedirects(response, reverse_lazy('journal:entry_detail', kwargs={'pk': self.entry1.pk}))
        assert len(response.context['messages']) > 0

    def test_wrong_delete_view(self):
        # Tests that someone can't delete another persons Entry
        self.client.force_login(user=self.entry2.user)
        response = self.client.get(
            reverse_lazy('journal:entry_delete', kwargs={'pk': self.entry1.uuid}),
            follow=True
        )
        self.assertEqual(response.status_code, 200, "Wrong Entry Delete Success redirect")
        self.assertTemplateNotUsed('journal:entry_delete')
        self.assertTemplateUsed('journal:entry_list')

    def test_delete_view_success(self):
        # Tests that someone can delete successfully
        response = self.client.get(
            reverse_lazy('journal:entry_delete', kwargs={'pk': self.entry1.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200, "Entry Delete")

    # TODO create scheduled test view


class TestContactViews(TestCase):
    # These tests are for contact views
    def setUp(self):
        # Every test needs access to the request factory
        self.user = UserFactory()
        self.subscribed_customer = create_active_subscriber(self.user)
        self.user.last_checkin = REFERENCE_DATE
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
            reverse_lazy('journal:released_entries', kwargs={'contact': self.contact.uuid}),
        )

        self.assertEqual(response.status_code, 200, "Released Entries List Page")
        self.assertTemplateUsed(response, 'journal/entry_list.html')

    def test_entries_released_detail(self):
        # Tests that a contact can visit an Entry detail page after being released
        self.client = Client()
        response = self.client.get(
            reverse_lazy('journal:released_entry_detail',
                    kwargs={'contact': self.contact.uuid, 'pk': self.entry_with_contact.pk}
                    ),
        )
        self.assertEqual(response.status_code, 200, "Released Entries Detail Page")
        self.assertTemplateUsed(response, 'journal/entry_detail.html')
