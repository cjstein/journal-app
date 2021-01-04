from django.contrib.auth.mixins import UserPassesTestMixin


class UserHasSubscriptionTest(UserPassesTestMixin):
    login_url = 'subscription:home'
    raise_exception = False
    redirect_field_name = 'subscription:home'
    permission_denied_message = "Please activate your subscription."

    def test_func(self):

        return self.request.user.subscription.status == 'trialing' or self.request.user.subscription.status == 'active'

