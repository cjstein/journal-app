# Django imports
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# Custom imports
from .models import Entry


# Entry Views
class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
