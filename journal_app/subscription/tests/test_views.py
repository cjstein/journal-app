import pytest
from django.test import TestCase, Client
from django.urls import reverse
from journal_app.subscription.tests.factories import TrialSubscriberFactory

pytestmark = pytest.mark.django_db


class TestSubscriptionViews(TestCase):
    # Test the views that are meant for the subscriptions
    def setUp(self) -> None:
        self.customer = TrialSubscriberFactory()
        self.user = self.customer.user
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_subscription_home_view(self):
        # Tests the view for the subscription home including the creation of the stripe customer
        self.assertIsNone(self.customer.stripe_customer_id)
        response = self.client.get(reverse('subscription:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(self.customer.stripe_customer_id)
        self.assertTemplateUsed(response, 'home.html')
