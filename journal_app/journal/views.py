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

    fields = [
        'title',
        'body',
    ]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(self).form_valid(form)


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry

    fields = [
        'title',
        'body',
    ]
    action = 'Update'


# Contact Pages
class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact

    fields = [
        'name',
        'email',
        'phone',
        'password',
    ]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(self).form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact

    fields = [
        'name',
        'email',
        'phone',
        'password',
    ]
    action = 'Update'

