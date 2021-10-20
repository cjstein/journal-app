from django.core import mail
from django.core.validators import RegexValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from twilio.rest import Client

from config.settings.base import (DEFAULT_FROM_EMAIL, TWILIO_ACCOUNT_SID,
                                  TWILIO_AUTH_TOKEN, TWILIO_NUMBER)
from journal_app.journal.models import Contact
from journal_app.users.models import User

phone_regex = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be 10 digits long with no spaces, dashes, or parenthesis",
)


class Mail(models.Model):
    """
    Email model to log and send all emails.
    In order to send an email, the following kwargs are required:
    user: User model instance
    subject: string for the subject line
    header: string for the header banner in the email. max_length=50
    template_name: just the name of the html template, found in the 'account/email/' template folder.  leave off .html
    context: as dictionary, if any other information is needed in the template beside any user info.

    The body of the email shall be created in the template for the email with the variables needed in them
    """

    subject = models.CharField(max_length=100, blank=True, null=True)
    header = models.CharField(max_length=100)
    to = models.EmailField(blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    email_from = models.EmailField(default=DEFAULT_FROM_EMAIL)
    html_message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    template_name = models.CharField(max_length=40, blank=False, null=False)

    def message(self, **context):
        context['user'] = self.user
        context['header'] = self.header
        self.html_message = render_to_string(self.get_full_template(), context)
        self.save()
        self.send_mail()
        return

    @property
    def plain_message(self):
        return strip_tags(self.html_message)

    def get_full_template(self):
        return f'account/email/{self.template_name}.html'

    def send_mail(self):
        mail.send_mail(self.subject, self.plain_message, None, [self.to], html_message=self.html_message)
        return

    def save(self, *args, **kwargs):
        if not self.to:
            self.to = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}: {self.template_name}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.user}, {self.template_name}, {self.datetime})'


# Text message model

class TextMessage(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField(blank=False)
    number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    sent_on = models.DateTimeField(blank=True, null=True)
    sid = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.contact}'

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.contact.phone
        super().save(*args, **kwargs)

    @property
    def to(self):
        return f'+1{self.number}'

    def send_text(self):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=self.body,
            from_=TWILIO_NUMBER,
            to=self.to,
        )
        self.sid = message.sid
        self.sent_on = timezone.now()
        self.status = message.status
        self.error_message = message.error_message
        self.save()
