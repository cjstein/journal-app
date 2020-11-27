import stripe
from django.conf import settings
from django.db import models
from django.utils.timezone import datetime

from journal_app.users.models import User


class StripeCustomer(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        TRIAL = "trial", "Trial"
        CANCELLED = "cancelled", "Cancelled"
        UNPAID = "unpaid", "Unpaid"
        INCOMPLETE = "incomplete", "Incomplete"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.TRIAL)
    subscription_start = models.DateTimeField(blank=True, null=True)
    subscription_end = models.DateTimeField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    product = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_subscription_status(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        self.product = stripe.Product.retrieve(subscription.plan.product)
        self.product_name = self.product.name
        self.subscription_end = datetime.fromtimestamp(subscription.current_period_end)
        self.subscription_start = datetime.fromtimestamp(subscription.current_period_start)
        self.status = subscription.status
        self.save()
