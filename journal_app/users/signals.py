from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

import stripe
from allauth.account.signals import email_confirmed

from journal_app.subscription.models import StripeCustomer
from journal_app.users.models import User

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


@receiver(email_confirmed)
def user_email_confirmed(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True
    user.save()
