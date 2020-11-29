from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.defaultfilters import date
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, RedirectView, UpdateView

from journal_app.journal.models import Entry
from journal_app.users.utils import user_viewing_own_profile

User = get_user_model()


class UserDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):

    model = User

    def get_object(self):
        return User.objects.get(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.get_object()
        return context

    def test_func(self):
        return user_viewing_own_profile(self.request, self.kwargs['username'])


user_detail_view = UserDetailView.as_view()


class UserUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={'username': self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "Information successfully updated"
        )
        return super().form_valid(form)

    def test_func(self):
        return user_viewing_own_profile(self.request, self.kwargs['username'])


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={'username': self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserCheckinView(UserPassesTestMixin, LoginRequiredMixin, RedirectView):
    url = reverse_lazy('journal:entry_list')

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def get_redirect_url(self, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        user.last_checkin = timezone.now()
        user.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'Thanks for checking in. Your next deadline is {date(user.checkin_deadline, "SHORT_DATE_FORMAT")}.'
        )
        return super().get_redirect_url(*args, **kwargs)

    def test_func(self):
        return user_viewing_own_profile(self.request, self.kwargs['username'])


user_checkin_view = UserCheckinView.as_view()


class AnonUserCheckinView(RedirectView):
    url = reverse_lazy('home')

    def get_redirect_url(self, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        if user.checkin_link == self.kwargs['uuid']:
            user.last_checkin = timezone.now()
            user.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                f'Thanks for checking in. Your next deadline is {date(user.checkin_deadline, "SHORT_DATE_FORMAT")}.'
            )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'There seems to be an issue with your checkin, please try again or contact us.'
            )
        return super().get_redirect_url(*args, **kwargs)


anon_user_checkin_view = AnonUserCheckinView.as_view()


class RetractPosts(UserPassesTestMixin, LoginRequiredMixin, RedirectView):

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def get_redirect_url(self, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "You Entries have been retracted"
        )
        entries = Entry.objects.filter(user=user)
        for entry in entries:
            entry.released = False
        Entry.objects.bulk_update(entries, ['released'])
        user.entries_released = False
        user.last_checkin = timezone.now()
        user.save()
        return reverse("users:detail", kwargs={'username': self.request.user.username})

    def test_func(self):
        return user_viewing_own_profile(self.request, self.kwargs['username'])


retract_posts_view = RetractPosts.as_view()


class ProfileSettings(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = User
    fields = ['days_to_release_setting']
    template_name = "users/user_settings_form.html"
    url = reverse_lazy("users:detail")

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "Information successfully updated"
        )
        return super().form_valid(form)

    def test_func(self):
        return user_viewing_own_profile(self.request, self.kwargs['username'])


settings_update_view = ProfileSettings.as_view()
