from django.core.management.base import BaseCommand
from journal_app.users.models import User
from journal_app.journal_mail.models import Mail


class Command(BaseCommand):
    help = "Checks each user's last check in and sends them a reminder email if it is within 5, 3 and 1 days"

    def handle(self, *args, **options):
        users = User.objects.filter(days_until_release__gt=0, days_until_release__lte=5)
        # users = User.objects.exclude(entries_released=True, days_until_release__gt=5, days_until_release__lt=1)
        subject = 'Checkin Deadline Approaching'
        for user in users:
            mail = Mail(
                user=user,
                subject=subject,
                header=subject,
                template_name='reminder_email'
            )
            mail.message()
