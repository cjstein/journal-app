# Django imports
from django.contrib import messages
from django.urls import reverse_lazy
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
        messages.add_message(self.request, messages.SUCCESS, 'Entry successfully added')
        form.instance.user = self.request.user
        return super().form_valid(form)


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry

    fields = [
        'title',
        'body',
    ]
    action = 'Update'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Entry successfully updated')
        return super().form_valid(form)


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
        messages.add_message(self.request, messages.SUCCESS, 'Contact successfully added')
        form.instance.user = self.request.user
        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact

    fields = [
        'name',
        'email',
        'phone',
        'password',
    ]
    action = 'Update'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Contact successfully updated')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('journal:contact_detail', kwargs={'pk': self.kwargs['pk']})
