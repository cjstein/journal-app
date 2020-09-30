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


class Entry(TimeStampedModel):
    """
    Entries for Journal.
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.__class__.__name__}({self.user}, {self.created}, {self.title})'
