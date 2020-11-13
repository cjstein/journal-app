# Python base imports
import uuid

# Django imports
from django.db import models
from django.urls import reverse

# Custom imports
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
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Fields below will only need at least one filled out
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    # Possibly add whatsapp bot
    # Possibly add Telegrambot
    # Possibly add signal bot

    def get_absolute_url(self):
        return reverse("journal:contact_entry_list", kwargs={"pk": self.uuid})

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.user}, {self.name})'

    class Meta:
        ordering = ['name']


class Entry(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField()
    # Released field changes once the 'release event has been triggered by the user.
    released = models.BooleanField(default=False)
    # If Public is flagged as True, when the posts get released, these entries will be viewable by all contacts.
    public = models.BooleanField(default=False)
    contact = models.ManyToManyField(Contact, blank=True)

    def get_absolute_url(self):
        return reverse("journal:entry_detail", kwargs={"pk": self.uuid})

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.__class__.__name__}({self.user}, {self.title})'

    class Meta:
        verbose_name = 'entry'
        verbose_name_plural = 'entries'
        ordering = ['-updated']
