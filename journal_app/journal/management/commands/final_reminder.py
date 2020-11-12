from django.core.management.base import BaseCommand
from django.utils import timezone

from journal_app.users.models import User

TODAY = timezone.now()

class Command(BaseCommand):
    help = "Checks each user's last check in and sends them a reminder email if it is the day before their release"

    def handle(self, *args, **options):
        pass
