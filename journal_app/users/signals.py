import stripe
from string import ascii_letters
from random import choice
from allauth.account.signals import email_confirmed
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from journal_app.users.models import User
from journal_app.subscription.models import StripeCustomer


@receiver(post_save, sender=User)
def create_stripe_customer(sender, instance, created, **kwargs):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if created:
        customer = StripeCustomer.objects.create(user=instance)
        if settings.DEBUG:
            choices = ''.join(str(i) for i in range(10)) + ascii_letters
            random_customer_string = ''.join(choice(choices) for i in range(14))
            customer.stripe_customer_id = f'cus_{random_customer_string}'
        else:
            stripe_customer = stripe.Customer.create(
                email=instance.email,
                description=str(instance),
            )
            customer.stripe_customer_id = stripe_customer.stripe_id
        customer.save()


@receiver(email_confirmed)
def user_email_confirmed(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True
    user.save()
