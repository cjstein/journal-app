from django.core.management.base import BaseCommand

from journal_app.journal_mail.models import Mail
from journal_app.users.models import User


class Command(BaseCommand):
    help = "Checks each user's last check in and sends them a reminder email if it is the day before their release"

    def handle(self, *args, **options):
        subject = 'Final warning before release'
        for user in User.objects.filter(entries_released=False):
            if user.days_until_release < 2:
                mail = Mail(
                    user=user,
                    subject=subject,
                    header=subject,
                    template_name='final_reminder_email'
                )
                mail.message()
                mail.save()
