import stripe
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from journal_app.users.models import User
from journal_app.subscription.models import StripeCustomer


@receiver(post_save, sender=User)
def create_stripe_customer(sender, instance, created, **kwargs):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if created:
        customer = stripe.Customer.create()
        subscription = stripe.Subscription.create(
            customer=customer.stripe_id,
            items=[
                {'price': 'price_1HllJ9EAWjMWH1XhSD8lRewP'},
            ],
            trial_period_days=14
        )
        stripe_customer = StripeCustomer.objects.create(
            user=instance,
            stripe_customer_id=customer.stripe_id,
            stripe_subscription_id=subscription.stripe_id,
        )
        stripe_customer.save()
        stripe_customer.get_subscription_status()
