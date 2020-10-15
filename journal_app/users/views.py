from datetime import datetime
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, "Information successfully updated"
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserCheckinView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        if user.username == self.kwargs['username'] and user.checkin_link == self.kwargs['checkin_link']:
            user.last_checkin = timezone.now()
            user.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                f'Thanks for checking in. Your next deadline is {datetime.strftime(user.checkin_deadline, "%h-%d-%Y %H:%M")}'
            )
            return reverse('journal:entry_list')
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'There seems to be an issue with your checkin, please try again or contact us.'
            )
            return reverse('journal:entry_list')


user_checkin_view = UserCheckinView.as_view()
