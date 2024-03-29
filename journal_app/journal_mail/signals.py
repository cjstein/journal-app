from django.dispatch import receiver

from allauth.account.signals import email_confirmed

from journal_app.journal_mail.models import Mail
from journal_app.users.models import User


@receiver(email_confirmed)
def user_confirmed_email(request, email_address, **kwargs):
    # Once the user confirms email, send them a welcome email
    user = User.objects.get(email=email_address.email)
    subject = 'Welcome to the Time Capsule Journal!'
    mail = Mail.objects.create(
        user=user,
        subject=subject,
        header=subject,
        template_name='welcome_email',
    )
    mail.message()
