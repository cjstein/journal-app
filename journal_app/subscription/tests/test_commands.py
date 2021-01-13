from io import StringIO
import pytest
from django.core.management import call_command
from django.test import TestCase
from journal_app.subscription.models import StripeCustomer
from journal_app.users.tests.factories import UserFactory
from journal_app.journal.tests.test_views import REFERENCE_DATE


pytestmark = pytest.mark.django_db


class TestTrialEndCommand(TestCase):
    """ Create two different user one where a trial ends and one where it should and make sure they all work correctly.
    """
    def setUp(self):
        self.active_user = UserFactory()
        self.second_active_user = UserFactory()
        self.expired_user = UserFactory()
        self.expired_user.subscription.trial_end = REFERENCE_DATE
        self.expired_user.subscription.status = StripeCustomer.Status.CANCELLED
        self.expired_user.subscription.save()

    def refresh_users_from_db(self):
        self.active_user.refresh_from_db()
        self.second_active_user.refresh_from_db()
        self.expired_user.refresh_from_db()

    def test_setup(self):
        self.refresh_users_from_db()
        self.assertEqual(self.active_user.subscription.status, 'trialing')
        self.assertEqual(self.second_active_user.subscription.status, 'trialing')
        self.assertEqual(self.expired_user.subscription.status, 'cancelled')

    def call_command(self, *args, **kwargs):
        """
        This calls the trial_end command
        """
        out = StringIO()
        call_command(
            'end_trial',
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def test_trial_end_command(self):
        self.active_user.subscription.trial_end = REFERENCE_DATE
        self.active_user.subscription.save()
        self.call_command()
        self.active_user_subscription = StripeCustomer.objects.get(user=self.active_user)
        self.second_active_user_subscription = StripeCustomer.objects.get(user=self.second_active_user)
        self.expired_user_subscription = StripeCustomer.objects.get(user=self.expired_user)
        self.assertEqual(self.active_user_subscription.status, 'cancelled')
        self.assertEqual(self.second_active_user_subscription.status, 'trialing')
        self.assertEqual(self.expired_user_subscription.status, 'cancelled')




