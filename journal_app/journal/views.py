from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from journal_app.journal.forms import ContactForm, EntryForm
from journal_app.journal.mixins import UserHasSubscriptionTest
from journal_app.journal.models import Contact, Entry
from journal_app.journal.utils import test_user_owns, get_entries_from_contact


# Entry Views
class EntryDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Entry
    redirect_field_name = 'journal:entry_list'

    def test_func(self):
        return test_user_owns(self.request, Entry, self.kwargs['pk'])

    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, 'Unable to find entry!')
        return super(EntryDetailView, self).handle_no_permission()


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    paginate_by = 15
    context_object_name = "entries"

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


class EntryUpdateView(UserHasSubscriptionTest, LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    raise_exception = True

    action = 'Update'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(EntryUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Entry successfully updated')
        instance = super().form_valid(form)
        entry = Entry.objects.get(uuid=self.kwargs['pk'])
        entry.updated = timezone.now()
        entry.save()
        return instance

    def get_context_data(self, **kwargs):
        context = super(EntryUpdateView, self).get_context_data()
        context['contacts'] = Contact.objects.filter(user=self.request.user)
        return context


class EntryDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'journal/entry_delete.html'
    raise_exception = True

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Entry Successfully deleted!')
        return reverse_lazy('journal:entry_list')

    def test_func(self):
        return test_user_owns(self.request, Entry, self.kwargs['pk'])


# Contact Pages


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


class ContactUpdateView(UserHasSubscriptionTest, LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm

    action = 'Update'

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
    paginate_by = 15
    context_object_name = "entries"

    def test_func(self):
        return test_user_owns(self.request, Contact, self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(get_entries_from_contact(self.kwargs['pk']))
        return context

    def get_queryset(self, *args, **kwargs):
        contact = Contact.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        return contact.entry_set.all()


class ContactReleasedEntryList(ListView):
    model = Entry
    template_name = 'journal/entry_list.html'
    paginate_by = 15
    login_url = 'home'
    raise_exception = False
    context_object_name = "entries"
    redirect_field_name = 'home'
    permission_denied_message = "That place you tried to reach isn't available. "

    def get_queryset(self, *args, **kwargs):
        contact = Contact.objects.get(pk=self.kwargs['contact'])
        return contact.user.entry_set.all().filter(public=True, released=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(get_entries_from_contact(self.kwargs['contact']))
        context['released'] = True
        return context


class ContactReleasedEntryDetail(UserPassesTestMixin, DetailView):
    model = Entry
    template_name = 'journal/entry_detail.html'
    login_url = 'home'
    raise_exception = False
    redirect_field_name = 'home'
    permission_denied_message = "That place you tried to reach isn't available."

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(get_entries_from_contact(self.kwargs['contact']))
        context['released'] = True
        return context
