from django.conf import settings
from django.core.management.base import BaseCommand

import stripe

from journal_app.journal.models import Entry
from journal_app.journal_mail.models import Mail, TextMessage
from journal_app.users.models import User
from journal_app.utils.bitly import shortener


class Command(BaseCommand):
    help = "Checks user last checkin and if it is past due, it releases their entries"

    def handle(self, *args, **options):
        users = User.objects.filter(entries_released=False, email_verified=True)
        for user in users:
            if user.release_entries:
                entries = Entry.objects.filter(user=user, is_scheduled=False)
                for entry in entries:
                    entry.released = True
                    entry.save()
                user.entries_released = True
                user.save()
                for contact in user.contact_set.all():
                    if contact.entry_set.all():
                        if contact.email and user.email_verified:
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
                            # Sends the contact a text with the bitly link to the site
                            url = shortener(contact.released_entries_url())
                            body = f'{user} has shared entries with you on Time Capsule Journal.  Click {url} to view.'
                            message = TextMessage.objects.create(
                                user=user,
                                contact=contact,
                                body=body
                            )
                            message.send_text()
                            message.save()
                try:
                    stripe.api_key = settings.STRIPE_SECRET_KEY
                    subscription = stripe.Subscription.retrieve(user.customer.stripe_subscription_id)
                    subscription['cancel_at_period_end'] = True
                    subscription.save()
                except Exception as e:
                    pass
                user_mail = Mail.objects.create(
                    user=user,
                    subject='Your entries have been released',
                    header='Your entries have been released',
                    template_name='entries_released',
                )
                user_mail.message()
