import pytest
from django.utils import timezone

from journal_app.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_user_checkin_deadline(user: User):
    user.last_checkin = timezone.now()
    assert user.checkin_deadline == user.last_checkin + timezone.timedelta(days=user.days_to_release)
    assert user.checkin_deadline != user.last_checkin + timezone.timedelta(days=1000)


def test_release_entries(user: User):
    user.last_checkin = timezone.now()
    assert not user.release_entries
    user.last_checkin = timezone.now() - timezone.timedelta(days=user.days_to_release + 1)
    assert user.release_entries
