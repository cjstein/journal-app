# Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from dal import autocomplete
from journal_app.journal.forms import EntryForm, ContactForm
# Custom imports
from journal_app.journal.models import Entry, Contact


# Entry Views
class EntryDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Entry
    redirect_field_name = 'journal:entry_list'

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

    def test_func(self):
        # Test to make sure the user is the one who owns the entry
        entry = Entry.objects.filter(pk=self.kwargs['pk'])[0]
        return self.request.user == entry.user

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
        # Test to make sure the user is the one who owns the entry
        entry = Entry.objects.filter(pk=self.kwargs['pk'])
        return self.request.user == entry[0].user

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Entry successfully updated')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EntryUpdateView, self).get_context_data()
        context['contacts'] = Contact.objects.filter(user=self.request.user)
        return context


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'journal/entry_delete.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Entry Successfully deleted!')
        return reverse_lazy('journal:entry_list')


# Contact Pages


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact

    def test_func(self):
        # Test to make sure the user is the one who owns the entry
        contact = Contact.objects.filter(pk=self.kwargs['pk'])
        return self.request.user == contact[0].user

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
        # Test to make sure the user is the one who owns the entry
        contact = Contact.objects.filter(pk=self.kwargs['pk'])
        return self.request.user == contact[0].user

    def get_success_url(self):
        return reverse_lazy('journal:contact_detail', kwargs={'pk': self.kwargs['pk']})

    def handle_no_permission(self):
        return Http404()


class ContactAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Contact.objects.none()

        qs = Contact.objects.filter(user=self.request.user)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
