from django.urls import path
from .views import *

app_name = "journal"

urlpatterns = [
    # Entry urls
    path("", EntryListView.as_view(), name='entry_list_view'),
    path("entry/<uuid:uuid>", EntryDetailView.as_view(), name='entry_detail_view'),
    path("entry/new", EntryCreateView.as_view(), name='entry_create_view'),
    path("entry/<uuid:uuid>/update", EntryUpdateView.as_view(), name='entry_update_view'),
    # Contact urls
    path("contacts", ContactListView.as_view(), name='contact_list_view'),
    path("contact/<uuid:uuid>", ContactDetailView.as_view(), name='contact_detail_view'),
    path("contact/new", ContactCreateView.as_view(), name='contact_create_view'),
    path("contact/<uuid:uuid>/update", ContactUpdateView.as_view(), name='contact_update_view'),
]
