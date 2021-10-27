from django.core.management.base import BaseCommand
from django.utils import timezone

from journal_app.journal_mail.models import Mail
from journal_app.subscription.models import StripeCustomer


class Command(BaseCommand):
    help = "Reviews each user with an active subscription and sends an update"

    def handle(self, *args, **options):
        for customer in StripeCustomer.objects.filter(status=StripeCustomer.Status.ACTIVE):
            if customer.subscription_end - timezone.timedelta(days=7) < timezone.now():
                mail = Mail.objects.create(
                    user=customer.user,
                    subject="Subscription at Time Capsule Journal is ending soon!",
                    template_name='subscription_ending_warning',
                )
                mail.message()
