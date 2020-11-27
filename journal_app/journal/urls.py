from django.urls import path

from journal_app.journal.views import (
    ContactAutoComplete,
    ContactCreateView,
    ContactDeleteView,
    ContactEntryList,
    ContactListView,
    ContactReleasedEntryDetail,
    ContactReleasedEntryList,
    ContactUpdateView,
    EntryCreateView,
    EntryDeleteView,
    EntryDetailView,
    EntryListView,
    EntryUpdateView,
)

app_name = "journal"

urlpatterns = [
    # Entry urls
    path("entry/<uuid:pk>/", EntryDetailView.as_view(), name='entry_detail'),
    path("entry/new/", EntryCreateView.as_view(), name='entry_create'),
    path("entry/<uuid:pk>/update/", EntryUpdateView.as_view(), name='entry_update'),
    path("entry/<uuid:pk>/delete/", EntryDeleteView.as_view(), name='entry_delete'),
    # Contact urls
    path("contacts/", ContactListView.as_view(), name='contact_list'),
    path("contact/<uuid:pk>/entries/", ContactEntryList.as_view(), name='contact_entry_list'),
    path("contact/new/", ContactCreateView.as_view(), name='contact_create'),
    path("contact/<uuid:pk>/update/", ContactUpdateView.as_view(), name='contact_update'),
    path("contact/<uuid:pk>/delete/", ContactDeleteView.as_view(), name='contact_delete'),
    path("contact/auto-complete/", ContactAutoComplete.as_view(), name='contact-autocomplete'),
    # Released urls
    path("released/<uuid:contact>/", ContactReleasedEntryList.as_view(), name='released_entries'),
    path("released/<uuid:contact>/<uuid:pk>", ContactReleasedEntryDetail.as_view(), name='released_entry_detail'),
    path("", EntryListView.as_view(), name='entry_list'),
]
