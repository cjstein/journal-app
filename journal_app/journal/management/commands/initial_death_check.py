from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from journal_app.journal.models import Entry, Contact
from journal_app.users.models import User
from journal_app.journal_mail.models import Mail


class Command(BaseCommand):
    help = "Checks each user's last check in and sends them a reminder email"

    def handle(self, *args, **options):
        users = User.objects.all()
