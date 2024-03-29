import string
from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse_lazy

import pytest
from factory import fuzzy

from journal_app.subscription.tests.factories import create_trial_subscriber, create_active_subscriber
from journal_app.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestSubscriptionViews(TestCase):
    # Test the views that are meant for the subscriptions
    def setUp(self) -> None:
        self.user = UserFactory()
        self.customer = create_trial_subscriber(self.user)

        self.client = Client()
        self.client.force_login(user=self.user)

    @patch('stripe.Customer.create')
    def test_subscription_home_view(self, mock_create):
        return_value = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix="cus_")
        mock_create.return_value.id = f'{return_value}'
        # Tests the view for the subscription home including the creation of the stripe customer
        self.assertIsNone(self.customer.stripe_customer_id)
        response = self.client.get(reverse_lazy('subscription:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subscription/home.html')
        self.customer.refresh_from_db()
        self.assertIsNotNone(self.customer.stripe_customer_id)
