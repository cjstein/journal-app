from django.core.management.base import BaseCommand
from journal_app.journal.models import Entry
from journal_app.users.models import User


class Command(BaseCommand):
    help = "Checks user last checkin and if it is past due, it releases their entries"

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            if user.release_entries:
                entries = Entry.objects.filter(user=user)
                for entry in entries:
                    entry.released = True
                    entry.save()
                user.entries_released = True
                user.save()
