
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

import pytest

from journal_app.subscription.tests.factories import (
    create_active_subscriber, create_trial_subscriber, create_cancelled_subscriber
)
from journal_app.users.tests.test_views import REFERENCE_DATE
from journal_app.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestTrialEndCommand(TestCase):
    """ Create two different user one where a trial ends and one where it should and make sure they all work correctly.
    """
    def setUp(self):
        self.trial_user = UserFactory()
        self.active_user = UserFactory()
        self.cancelled_user = UserFactory()
        self.trial_customer = create_trial_subscriber(self.trial_user)
        self.active_customer = create_active_subscriber(self.active_user)
        self.cancelled_customer = create_cancelled_subscriber(self.cancelled_user)
        self.assertEqual(self.active_customer.status, 'active')
        self.assertEqual(self.trial_customer.status, 'trialing')
        self.assertEqual(self.cancelled_customer.status, 'cancelled')
        self.trial_customer.trial_end = REFERENCE_DATE
        self.trial_customer.save()
        self.refresh_users_from_db()
        self.call_command()
        self.refresh_users_from_db()

    def refresh_users_from_db(self):
        self.active_customer.refresh_from_db()
        self.trial_customer.refresh_from_db()
        self.cancelled_customer.refresh_from_db()

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

    def test_trial_end_command_on_active(self):
        self.assertEqual(self.active_customer.status, 'active')

    def test_trial_end_command_on_trial(self):
        self.assertEqual(self.trial_customer.status, 'cancelled')

    def test_trial_end_command_on_cancelled(self):
        self.assertEqual(self.cancelled_customer.status, 'cancelled')
