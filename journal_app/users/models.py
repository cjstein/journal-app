import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.db.models import (BooleanField, CharField, DateTimeField,
                              IntegerField, UUIDField)
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    """Default user for Journal App."""
    name = CharField(blank=True, max_length=255)
    checkin_link = UUIDField(default=uuid.uuid4)
    last_checkin = DateTimeField(default=timezone.now)
    days_to_release_setting = IntegerField(default=7)
    entries_released = BooleanField(default=False)
    email_verified = BooleanField(default=False)

    def get_absolute_url(self):
        domain = Site.objects.get_current().domain
        return domain + reverse("users:detail", kwargs={"username": self.username})

    @property
    def checkin_deadline(self):
        return self.last_checkin + timezone.timedelta(days=self.days_to_release_setting)

    @property
    def release_entries(self):
        """
        This function returns a boolean based on if the desired number of days has passed since last check in.
        """
        return timezone.now() > self.checkin_deadline

    @property
    def days_until_release(self):
        return (self.checkin_deadline - timezone.now()).days

    def get_absolute_checkin_link(self):
        domain = Site.objects.get_current().domain
        url = reverse('users:anon_checkin',
                      kwargs={'username': self.username,
                              'uuid': self.checkin_link},
                      )
        return f"{domain}{url}"

    def __str__(self):
        return self.name or self.username
