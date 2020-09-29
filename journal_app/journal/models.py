import uuid
from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def modified(self):
        return self.updated != self.created

    class Meta:
        abstract = True


class Entry(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=False)
