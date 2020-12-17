from django.core.management.base import BaseCommand

from journal_app.journal.models import Entry
from journal_app.journal_mail.models import Mail
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
                for contact in user.contact_set.all():
                    if contact.entry_set.all():
                        if contact.email:
                            subject = f"{user} has shared memories with you, read them here"
                            contact_mail = Mail(
                                user=user,
                                subject=subject,
                                to=contact.email,
                                header=subject,
                                template_name='release_to_contact'
                            )
                            contact_mail.save()
                            contact_mail.message(contact=contact)
                        if contact.phone:
                            # TODO add phone method for notifying contact
                            pass
                user_mail = Mail.objects.create(
                    user=user,
                    subject='Your entries have been released',
                    header='Your entries have been released',
                    template_name='entries_released',
                )
                user_mail.message()
