# Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from dal import autocomplete
from journal_app.journal.forms import EntryForm, ContactForm
# Custom imports
from journal_app.journal.models import Entry, Contact


def test_user_owns(request, model: models.Model, pk):
    test_model = model.objects.filter(pk=pk)[0]
    return request.user == test_model.user


# Entry Views
class EntryDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Entry
    redirect_field_name = 'journal:entry_list'

    def get_queryset(self):
        user_entries = Entry.objects.filter(user=self.request.user)
        return user_entries

    def test_func(self):
        return test_user_owns(self.request, Entry, self.kwargs['pk'])

    def handle_no_permission(self):
        # messages.add_message(self.request, messages.ERROR, 'Unable to find entry!')
        return super(EntryDetailView, self).handle_no_permission()


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(EntryCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Entry successfully added')
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView, self).get_context_data()
        context['contacts'] = Contact.objects.filter(user=self.request.user)
        return context


class EntryUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    raise_exception = True

    action = 'Update'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(EntryUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return test_user_owns(self.request, Entry, self.kwargs['pk'])

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Entry successfully updated')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EntryUpdateView, self).get_context_data()
        context['contacts'] = Contact.objects.filter(user=self.request.user)
        return context


class EntryDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'journal/entry_delete.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Entry Successfully deleted!')
        return reverse_lazy('journal:entry_list')

    def test_func(self):
        return test_user_owns(self.request, Entry, self.kwargs['pk'])


# Contact Pages


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact

    def test_func(self):
        return test_user_owns(self.request, Contact, self.kwargs['pk'])

    def handle_no_permission(self):
        return Http404()


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Contact successfully added')
        form.instance.user = self.request.user
        return super().form_valid(form)


class ContactUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm

    action = 'Update'

    def test_func(self):
        return test_user_owns(self.request, Contact, self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('journal:contact_detail', kwargs={'pk': self.kwargs['pk']})

    def handle_no_permission(self):
        return Http404()


class ContactDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'journal/contact_delete.html'

    def test_func(self):
        return test_user_owns(self.request, Contact, self.kwargs['pk'])

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Contact Successfully deleted!')
        return reverse_lazy('journal:contact_list')


class ContactAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Contact.objects.none()

        qs = Contact.objects.filter(user=self.request.user)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class ContactEntryList(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'journal/contact_entry_list.html'

    def test_func(self):
        return test_user_owns(self.request, Contact, self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        contact = Contact.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        entry_list = contact.entry_set.all()
        context['contact'] = contact
        context['entry_list'] = entry_list
        return context


class ContactReleasedEntryList(UserPassesTestMixin, ListView):
    model = Entry
    template_name = 'journal/entry_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        contact = Contact.objects.get(pk=self.kwargs['contact'])
        entry_list = contact.entry_set.all()
        context['contact'] = contact
        context['entry_list'] = entry_list
        context['released'] = True
        return context

    def test_func(self):
        contact = Contact.objects.get(pk=self.kwargs['contact'])
        return contact.user.entries_released


class ContactReleasedEntryDetail(UserPassesTestMixin, DetailView):
    model = Entry
    template_name = 'journal/entry_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        contact = Contact.objects.get(pk=self.kwargs['contact'])
        entry_list = contact.entry_set.all()
        context['contact'] = contact
        context['entry_list'] = entry_list
        context['released'] = True
        return context

    def test_func(self):
        contact = Contact.objects.get(pk=self.kwargs['contact'])
        return contact.user.entries_released
