import datetime

from django.core.management.base import BaseCommand

from journal_app.journal.models import Entry
from journal_app.journal_mail.models import Mail, TextMessage
from journal_app.utils.bitly import shortener
from journal_app.users.models import User


class Command(BaseCommand):
    help = "Checks the scheduled entries and releases the ones that are due to release"

    def handle(self, *args, **options):
        entries = Entry.objects.filter(is_scheduled=True, released=False, scheduled_time__lte=datetime.date.today)
        for entry in entries:
            for contact in entry.contact_set.all():
                if contact.entry_set.all():
                    if contact.email and entry.user.email_verified:
                        subject = f"{entry.user} has shared a journal entry with you, read them here!"
                        contact_mail = Mail(
                            user=entry.user,
                            subject=subject,
                            to=contact.email,
                            header=subject,
                            template_name='release_to_contact'
                        )
                        contact_mail.save()
                        contact_mail.message(contact=contact)
                    if contact.phone:
                        # Sends the contact a text with the bitly link to the site
                        url = shortener(contact.released_entries_url)
                        body = f'{entry.user} has shared entries with you on Time Capsule Journal.  Click {url} to view.'
                        message = TextMessage.objects.create(
                            user=entry.user,
                            contact=contact,
                            body=body
                        )
                        message.send_text()
                        message.save()
            user_mail = Mail.objects.create(
                user=entry.user,
                subject='Your scheduled entry has been released',
                header='Your scheduled entry has been released',
                template_name='entries_released',
            )
            user_mail.message()
