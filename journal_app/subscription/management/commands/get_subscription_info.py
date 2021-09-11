from django.core.management.base import BaseCommand

from journal_app.subscription.models import StripeCustomer, Subscription
from journal_app.users.models import User


class Command(BaseCommand):
    help = "Retrieve the subscription information from the Stripe API"

    def handle(self, *args, **options):
        for user in User.objects.all():
            print(f'{user}::{user.customer.stripe_customer_id}::{user.customer.stripe_subscription_id}')
            try:
                customer = user.customer
                customer.get_subscription_status()
                customer.save()
            except StripeCustomer.DoesNotExist:
                pass
            except Subscription.DoesNotExist:
                pass
