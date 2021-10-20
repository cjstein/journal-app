from django.conf import settings
from django.urls import reverse


def test_subscription_home_url():
    assert reverse('subscription:home') == '/subscription/'


def test_success_url():
    assert reverse('subscription:success') == '/subscription/success/'


def test_cancel_url():
    assert reverse('subscription:cancel') == '/subscription/cancel/'


def test_webhook_url():
    assert reverse('subscription:webhook') == f'/subscription/{settings.WEBHOOK_URL}'
