import stripe
from django.conf import settings
from django.db import models
from django.utils import timezone

from journal_app.users.models import User


def trial_end_date(days=14):
    now = timezone.now()
    return now + timezone.timedelta(days=days)


class StripeCustomer(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        TRIAL = "trialing", "Trial"
        CANCELLED = "cancelled", "Cancelled"
        UNPAID = "unpaid", "Unpaid"
        INCOMPLETE = "incomplete", "Incomplete"
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.TRIAL)
    trial_end = models.DateTimeField(default=trial_end_date)
    subscription_start = models.DateTimeField(blank=True, null=True)
    subscription_end = models.DateTimeField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    product = models.TextField(blank=True, null=True)
    subscription_cache = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_subscription_status(self):
        if self.stripe_subscription_id:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
            self.product = stripe.Product.retrieve(subscription.plan.product)
            self.product_name = self.product.name
            self.subscription_end = timezone.datetime.fromtimestamp(subscription.current_period_end)
            self.subscription_start = timezone.datetime.fromtimestamp(subscription.current_period_start)
            self.status = subscription.status
            self.subscription_cache = subscription
            self.save()
        else:
            if self.trial_end < timezone.now():
                self.status = self.status.CANCELLED
                self.save()
