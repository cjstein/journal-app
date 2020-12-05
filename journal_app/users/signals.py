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
        customer = StripeCustomer.objects.create()
