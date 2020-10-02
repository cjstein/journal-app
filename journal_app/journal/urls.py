from django.urls import path
from .views import *

app_name = "journal"

urlpatterns = [
    # Entry urls
    path("", EntryListView.as_view(), name='entry_list'),
    path("entry/<uuid:uuid>", EntryDetailView.as_view(), name='entry_detail'),
    path("entry/new", EntryCreateView.as_view(), name='entry_create'),
    path("entry/<uuid:uuid>/update", EntryUpdateView.as_view(), name='entry_update'),
    # Contact urls
    path("contacts", ContactListView.as_view(), name='contact_list'),
    path("contact/<uuid:uuid>", ContactDetailView.as_view(), name='contact_detail'),
    path("contact/new", ContactCreateView.as_view(), name='contact_create'),
    path("contact/<uuid:uuid>/update", ContactUpdateView.as_view(), name='contact_update'),
]
