# Django imports
# from django.shortcuts import render
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Custom imports
from .models import Entry, Contact


# Entry Views
class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
