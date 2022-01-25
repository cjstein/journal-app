import stripe
import string
from allauth.account.signals import email_confirmed
from factory import fuzzy
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from journal_app.users.models import User
from journal_app.subscription.models import StripeCustomer


# Trying to test mocking and not create stripe customers at every User instance
# @receiver(post_save, sender=User)
# def create_stripe_customer(sender, instance, created, **kwargs):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     if created:
#         customer = StripeCustomer.objects.create(user=instance)
#         stripe_customer = stripe.Customer.create(
#             email=instance.email,
#             description=str(instance),
#         )
#         customer.stripe_customer_id = stripe_customer.stripe_id
#         customer.save()

@receiver(post_save, sender=User)
def create_stripe_customer(sender, instance, created, **kwargs):
    if created:
        customer = StripeCustomer.objects.create(user=instance)
        customer.save()
