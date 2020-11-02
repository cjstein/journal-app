from django.db import models
from django.contrib.sites.models import Site
from allauth.account.signals import email_confirmed
from django.core import mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from journal_app.users.models import User

# Create your models here.
CURRENT_SITE_NAME = Site.objects.get_current().domain


@receiver(email_confirmed)
def user_confirmed_email(request, email_address, **kwargs):
    # Once the user confirms email, send them a welcome email
    user = User.objects.get(email=email_address.email)
    subject = f'Welcome to {CURRENT_SITE_NAME}!'
    html_message = render_to_string('account/email/welcome_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    to = user.email
    mail.send_mail(subject, plain_message, None, [to], html_message=html_message)
