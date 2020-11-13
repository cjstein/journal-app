import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    IntegerField,
    UUIDField,
)
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    """Default user for Journal App."""
    name = CharField(blank=True, max_length=255)
    checkin_link = UUIDField(default=uuid.uuid4)
    last_checkin = DateTimeField(default=timezone.now)
    # How many days after check-in until release.  This may be a customizable field in the future.
    days_to_release_setting = IntegerField(default=7)
    entries_released = BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

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
        return reverse("users:anon_checkin", kwargs={'username': self.username, 'uuid': self.checkin_link})

    def __str__(self):
        return self.name if self.name else self.username
