from django.core.management.base import BaseCommand

from journal_app.journal_mail.models import Mail
from journal_app.users.models import User

DAYS_FOR_REMINDER = 5


class Command(BaseCommand):
    help = "Checks each user's last check in and sends them a reminder email if it is within 5, 3 and 1 days"

    def handle(self, *args, **options):
        subject = 'Checkin Deadline Approaching'
        for user in User.objects.filter(entries_released=False, email_verified=True):
            if DAYS_FOR_REMINDER > user.days_until_release > 1:
                mail = Mail.objects.create(
                    user=user,
                    subject=subject,
                    header=subject,
                    template_name='reminder_email'
                )
                mail.message()

