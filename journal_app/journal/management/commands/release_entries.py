from django.core.management.base import BaseCommand
from journal_app.journal.models import Entry, Contact
from journal_app.users.models import User


class Command(BaseCommand):
    help = "Checks each user's last check in and sends them a reminder email"

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            if user.release_entries:
                entries = Entry.objects.filter(user=user)
                for entry in entries:
                    entry.released = True
                    entry.save()
