from io import StringIO
import pytest
from django.core.management import call_command
from django.test import TestCase
from journal_app.subscription.models import StripeCustomer
from journal_app.subscription.tests.factories import ActiveSubscriberFactory, ExpiredSubscriberFactory, TrialSubscriberFactory
from journal_app.journal.tests.test_views import REFERENCE_DATE


pytestmark = pytest.mark.django_db


class TestTrialEndCommand(TestCase):
    """ Create two different user one where a trial ends and one where it should and make sure they all work correctly.
    """
    def setUp(self):
        self.trial_customer = TrialSubscriberFactory()
        self.active_customer = ActiveSubscriberFactory()
        self.expired_customer = ExpiredSubscriberFactory()
        self.trial_user = self.trial_customer.user
        self.active_user = self.active_customer()
        self.expired_user = self.expired_customer.user
        self.expired_user.customer.trial_end = REFERENCE_DATE
        self.expired_user.customer.save()

    def refresh_users_from_db(self):
        self.active_user.refresh_from_db()
        self.trial_user.refresh_from_db()
        self.expired_user.refresh_from_db()

    def test_setup(self):
        self.refresh_users_from_db()
        self.assertEqual(self.active_user.customer.status, 'active')
        self.assertEqual(self.trial_user.customer.status, 'trialing')
        self.assertEqual(self.expired_user.customer.status, 'cancelled')

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
        self.trial_customer.trial_end = REFERENCE_DATE
        self.trial_customer.save()
        self.call_command()
        self.assertEqual(self.active_customer.status, 'active')
        self.assertEqual(self.trial_customer.status, 'cancelled')
        self.assertEqual(self.expired_customer.status, 'cancelled')




