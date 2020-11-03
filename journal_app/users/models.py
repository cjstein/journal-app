import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, UUIDField, DateTimeField, IntegerField, BooleanField
from django.urls import reverse
from django.utils import timezone
from django.core import mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.models import Site
from allauth.account.signals import email_confirmed


CURRENT_SITE_NAME = Site.objects.get_current().domain


class User(AbstractUser):
    """Default user for Journal App."""
    name = CharField(blank=True, max_length=255)
    checkin_link = UUIDField(default=uuid.uuid4)
    last_checkin = DateTimeField(default=timezone.now)
    # How many days after check-in until release.  This may be a customizable field in the future.
    days_to_release = IntegerField(default=7)
    entries_released = BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def checkin_deadline(self):
        return self.last_checkin + timezone.timedelta(days=self.days_to_release)

    @property
    def release_entries(self):
        """
        This function returns a boolean based on if the desired number of days has passed since last check in.
        """
        return timezone.now() > self.checkin_deadline

    def get_absolute_checkin_link(self):
        return reverse("users:anon_checkin", kwargs={'username': self.username, 'uuid': self.checkin_link})
