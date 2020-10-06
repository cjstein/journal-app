import pytest
from pytest_django.asserts import assertContains

from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from journal_app.users.models import User

from ..models import Entry, Contact
from ..views import (
    EntryCreateView, EntryUpdateView, EntryDetailView, EntryListView,
    ContactCreateView, ContactUpdateView, ContactDetailView, ContactListView,
)

pytestmark = pytest.mark.django_db

# Entry view Tests


def test_good_entry_list(rf):
    # Get the request
    request = rf.get(reverse("journal:entry_list"))
    # Use the request to get the response
    response = EntryListView.as_view()(request)
    # Test that response is valid
    assertContains(response, 'Entry List')


def test_good_entry_detail_view(rf, entry):
    # Get the request
    url = reverse('journal:entry_detail', kwargs={'uuid': entry.uuid})
    request = rf.get(url)
    # Use the request to get the response
    callable_obj = EntryDetailView.as_view()
    response = callable_obj(request, uuid=entry.uuid)
    # Test that the response is valid
    assertContains(response, entry.title)
