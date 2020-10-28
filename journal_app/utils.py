from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from config.settings.production import DEFAULT_FROM_EMAIL, EMAIL_SUBJECT_PREFIX


def email_welcome(to, **context):
    subject = f'Welcome to '
