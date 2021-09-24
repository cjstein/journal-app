from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    RedirectView,
)
from journal_app.journal.forms import ContactForm, EntryForm, EntryScheduleForm
from journal_app.journal.models import Contact, Entry
from journal_app.journal.utils import test_user_owns, test_user_has_subscription

# Entry Views
# -------------------------------------------------------------------------------------------------------


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


class EntryUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
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

    def test_func(self):
        owner_valid = test_user_owns(self.request, Entry, pk=self.kwargs['pk'])
        subscription_valid = test_user_has_subscription(self.request)
        return owner_valid and subscription_valid

    def handle_no_permission(self):
        owner_valid = test_user_owns(self.request, Entry, self.kwargs['pk'])
        subscription_valid = test_user_has_subscription(self.request)
        if subscription_valid and not owner_valid:
            messages.add_message(self.request, messages.ERROR, 'Unable to access that object')
            return redirect('journal:entry_list')

        if owner_valid and not subscription_valid:
            messages.add_message(self.request, messages.ERROR, 'Please activate your subscription')
            return redirect('subscription:home')


class EntryScheduleView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryScheduleForm
    raise_exception = True
    template_name = 'journal/entry_schedule.html'

    action = 'Update'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Entry successfully scheduled')
        instance = super().form_valid(form)
        entry = Entry.objects.get(uuid=self.kwargs['pk'])
        entry.updated = timezone.now()
        entry.is_scheduled = True
        entry.save()
        return instance

    def test_func(self):
        owner_valid = test_user_owns(self.request, Entry, self.kwargs['pk'])
        subscription_valid = test_user_has_subscription(self.request)
        return owner_valid and subscription_valid

    def handle_no_permission(self):
        owner_valid = test_user_owns(self.request, Entry, self.kwargs['pk'])
        subscription_valid = test_user_has_subscription(self.request)
        if subscription_valid and not owner_valid:
            messages.add_message(self.request, messages.ERROR, 'Unable to access that object')
            return redirect('journal:entry_list')

        if owner_valid and not subscription_valid:
            messages.add_message(self.request,
                                 messages.ERROR,
                                 'Please activate your subscription to schedule released entries',
                                 )
            return redirect('subscription:home')


class EntryDeleteView(UserPassesTestMixin, LoginRequiredMixin, RedirectView):

    def test_func(self):
        return test_user_owns(self.request, Entry, self.kwargs['pk'])

    def get_redirect_url(self, *args, **kwargs):
        entry = Entry.objects.get(pk=self.kwargs['pk'])
        title = entry.title
        entry.delete()
        messages.add_message(self.request, messages.SUCCESS, f"{title} successfully deleted!")
        return reverse_lazy('journal:entry_list')


# Contact Pages
# ------------------------------------------------------------------------------------------------------------


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm

    def form_valid(self, form):
        name = form.cleaned_data['name']
        messages.add_message(self.request, messages.SUCCESS, f'{name} successfully added')
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # messages.add_message(self.request, messages.SUCCESS, "")
        return reverse_lazy('journal:contact_list')


class ContactUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    action = 'Update'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        messages.add_message(self.request, messages.SUCCESS, f'{name} successfully updated')
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('journal:contact_list')

    def test_func(self):
        owner_valid = test_user_owns(self.request, Contact, self.kwargs['pk'])
        subscription_valid = test_user_has_subscription(self.request)
        return owner_valid and subscription_valid

    def handle_no_permission(self):
        owner_valid = test_user_owns(self.request, Contact, self.kwargs['pk'])
        subscription_valid = test_user_has_subscription(self.request)
        if subscription_valid and not owner_valid:
            messages.add_message(self.request, messages.ERROR, 'Unable to access that object')
            return redirect('journal:entry_list')

        if owner_valid and not subscription_valid:
            messages.add_message(self.request, messages.ERROR, 'Please activate your subscription')
            return redirect('users:settings')


class ContactDeleteView(UserPassesTestMixin, LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        contact = Contact.objects.get(pk=self.kwargs['pk'])
        name = contact.name
        contact.delete()
        messages.add_message(self.request, messages.SUCCESS, f"{name} successfully deleted!")
        return reverse_lazy('journal:contact_list')

    def test_func(self):
        return test_user_owns(self.request, Contact, self.kwargs['pk'])


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
        contact = Contact.objects.get(pk=self.kwargs['pk'])
        entry_list = contact.entry_set.all()
        public_list = contact.user.entry_set.all().filter(public=True)
        entries = entry_list | public_list
        context['entries'] = entries.order_by('created')
        context['contact'] = contact
        return context

    def get_queryset(self, *args, **kwargs):
        contact = Contact.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        return contact.entry_set.all()


# Released Views
# -----------------------------------------------------------------------------------------------------------------


class ContactReleasedEntryList(ListView):
    model = Entry
    template_name = 'journal/entry_list.html'
    paginate_by = 15
    context_object_name = "entries"

    def get_queryset(self, *args, **kwargs):
        contact = Contact.objects.get(pk=self.kwargs['contact'])
        contact_entries = contact.entry_set.all().filter(released=True)
        public = contact.user.entry_set.all().filter(public=True, released=True)
        combined = contact_entries | public
        return combined.order_by('created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        contact = Contact.objects.get(pk=self.kwargs['contact'])
        context['contact'] = contact
        contact_entries = contact.entry_set.all().filter(released=True)
        public = contact.user.entry_set.all().filter(public=True, released=True)
        combined = contact_entries | public
        context['entries'] = combined.order_by('created')
        context['released'] = True
        return context


class ContactReleasedEntryDetail(UserPassesTestMixin, DetailView):
    model = Entry
    template_name = 'journal/entry_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['contact'] = Contact.objects.get(pk=self.kwargs['contact'])
        context['entry'] = Entry.objects.get(pk=self.kwargs['pk'])
        context['released'] = True
        return context

    def test_func(self):
        contact = Contact.objects.get(pk=self.kwargs['contact'])
        return contact.user.entries_released
