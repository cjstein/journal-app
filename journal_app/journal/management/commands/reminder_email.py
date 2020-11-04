from django.core.management.base import BaseCommand
from journal_app.users.models import User
from journal_app.journal_mail.models import Mail

DAYS_FOR_REMINDER = 6


class Command(BaseCommand):
    help = "Checks each user's last check in and sends them a reminder email if it is within 5, 3 and 1 days"

    def handle(self, *args, **options):
        subject = 'Checkin Deadline Approaching'
        for user in User.objects.all():
            if not user.entries_released and user.days_until_release < DAYS_FOR_REMINDER:
                mail = Mail(
                    user=user,
                    subject=subject,
                    header=subject,
                    template_name='reminder_email'
                )
                mail.message()
                mail.save()
