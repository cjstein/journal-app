from django.core.management.base import BaseCommand
from django.utils import timezone

from journal_app.subscription.models import StripeCustomer
from journal_app.journal_mail.models import Mail


class Command(BaseCommand):
    help = "Reviews each user with a trial subscription and determines if it needs to cancel it"

    def handle(self, *args, **options):
        for customer in StripeCustomer.objects.filter(status=StripeCustomer.Status.TRIAL):
            if customer.trial_end < timezone.now():
                mail = Mail.objects.create(
                    user=customer.user,
                    subject="Trial has ended at Time Capsule Journal!",
                    template_name='trial_end',
                )
                mail.message()
                customer.status = StripeCustomer.Status.CANCELLED
                customer.save()
