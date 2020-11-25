from django.core.management.base import BaseCommand

from journal_app.subscription.models import StripeCustomer
from journal_app.users.models import User


class Command(BaseCommand):
    help = "Retrieve the subscription information from the Stripe API"

    def handle(self, *args, **options):
        for user in User.objects.all():
            try:
                customer = StripeCustomer.objects.get(user=user)
                customer.get_subscription_status()
            except StripeCustomer.DoesNotExist:
                pass
