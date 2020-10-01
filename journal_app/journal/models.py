import uuid
from django.db import models
from model_utils.fields import MonitorField
from journal_app.users.models import User


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def modified(self):
        return self.updated != self.created

    class Meta:
        abstract = True


class Contact(TimeStampedModel):
    """
    Contact model will be user supplied and all journal Entries that are tagged with that contact or "public" will be
    filtered when released.
    """
    name = models.CharField(max_length=255)
    # Fields below will only need at least one filled out
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15)
    # Possibly add whatsapp bot
    # Possibly add Telegrambot
    # Possibly add signal bot

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.email}, {self.password})'


class Entry(TimeStampedModel):
    """
    Entries for Journal.
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    released = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    contact = models.ManyToManyField(Contact,)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.__class__.__name__}({self.user}, {self.created}, {self.title})'
