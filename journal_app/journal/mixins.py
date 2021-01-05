from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect


class UserHasSubscriptionTest(UserPassesTestMixin):
    """
    This mixin tests whether the user has an active or trialing subscription and whether the user owns the object
    that is trying to be edited
    Note: only use this Mixin on Update views and is only valid for single object views
    """
    login_url = 'users:settings'
    raise_exception = True
    redirect_field_name = 'users:settings'
    permission_denied_message = "Please activate your subscription."

    @property
    def subscription_valid(self):
        # This tests whether the user has a valid subscription
        # A valid subscription is whether they have a trial or active subscription
        test_subscription = (
            self.request.user.subscription.status == 'trialing' or
            self.request.user.subscription.status == 'active'
        )
        return test_subscription

    @property
    def model_valid(self):
        # This test whether a user owns the model they are trying to access
        return self.request.user == self.model.user

    def test_func(self):
        return self.subscription_valid and self.model_valid

    def handle_no_permission(self):
        if self.subscription_valid and not self.model_valid:
            messages.add_message(self.request, messages.ERROR, 'Unable to access that object')
            return redirect('journal:entry_list')

        if self.model_valid and not self.subscription_valid:
            messages.add_message(self.request, messages.ERROR, 'Please activate your subscription')
            return redirect('users:settings')

