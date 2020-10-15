from django.urls import path
from journal_app.journal.views import (
    EntryCreateView, EntryListView, EntryDetailView, EntryUpdateView,
    ContactCreateView, ContactListView, ContactDetailView, ContactUpdateView,
)

app_name = "journal"

urlpatterns = [
    # Entry urls
    path("entry/<uuid:pk>/", EntryDetailView.as_view(), name='entry_detail'),
    path("entry/new/", EntryCreateView.as_view(), name='entry_create'),
    path("entry/<uuid:pk>/update/", EntryUpdateView.as_view(), name='entry_update'),
    # Contact urls
    path("contacts/", ContactListView.as_view(), name='contact_list'),
    path("contact/<uuid:pk>/", ContactDetailView.as_view(), name='contact_detail'),
    path("contact/new/", ContactCreateView.as_view(), name='contact_create'),
    path("contact/<uuid:pk>/update/", ContactUpdateView.as_view(), name='contact_update'),
    path("", EntryListView.as_view(), name='entry_list'),
]
