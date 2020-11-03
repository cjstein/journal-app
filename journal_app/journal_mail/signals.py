from django.dispatch import receiver
from django.contrib.sites.models import Site
from journal_app.journal_mail.models import Mail
from journal_app.users.models import User
from allauth.account.signals import email_confirmed


CURRENT_SITE_NAME = Site.objects.get_current().domain


@receiver(email_confirmed)
def user_confirmed_email(request, email_address, **kwargs):
    # Once the user confirms email, send them a welcome email
    user = User.objects.get(email=email_address.email)
    subject = f'Welcome to {CURRENT_SITE_NAME}!'
    mail = Mail(
        user=user,
        subject=subject,
        header=subject,
        template_name='welcome_email',
    )
    mail.message()

