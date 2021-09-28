from io import StringIO
import pytest
from django.core.management import call_command
from django.test import TestCase
from journal_app.subscription.models import StripeCustomer
from journal_app.subscription.tests.factories import ActiveSubscriberFactory, ExpiredSubscriberFactory, TrialSubscriberFactory
from journal_app.users.tests.test_views import REFERENCE_DATE


pytestmark = pytest.mark.django_db


class TestTrialEndCommand(TestCase):
    """ Create two different user one where a trial ends and one where it should and make sure they all work correctly.
    """
    def setUp(self):
        self.trial_customer = TrialSubscriberFactory()
        self.active_customer = ActiveSubscriberFactory()
        self.expired_customer = ExpiredSubscriberFactory()
        self.trial_customer.trial_end = REFERENCE_DATE
        self.trial_customer.save()

    def refresh_users_from_db(self):
        self.active_customer.refresh_from_db()
        self.trial_customer.refresh_from_db()
        self.expired_customer.refresh_from_db()

    def test_setup(self):
        self.refresh_users_from_db()
        self.assertEqual(self.active_customer.status, 'active')
        self.assertEqual(self.trial_customer.status, 'trialing')
        self.assertEqual(self.expired_customer.status, 'cancelled')

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
        self.call_command()
        self.refresh_users_from_db()
        self.assertEqual(self.active_customer.status, 'active')
        self.assertEqual(self.trial_customer.status, 'cancelled')
        self.assertEqual(self.expired_customer.status, 'cancelled')




