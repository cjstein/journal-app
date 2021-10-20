from django.contrib.sites.models import Site
from django.test import TestCase
from django.utils import timezone

import pytest

from journal_app.users.models import User
from journal_app.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    domain = Site.objects.get_current().domain
    assert user.get_absolute_url() == f"{domain}/users/{user.username}/"


def test_user_checkin_deadline(user: User):
    user.last_checkin = timezone.now()
    user.save()
    user.refresh_from_db()
    assert user.checkin_deadline == user.last_checkin + timezone.timedelta(days=user.days_to_release_setting)


def test_release_entries(user: User):
    user.last_checkin = timezone.now()
    user.save()
    user.refresh_from_db()
    assert not user.release_entries
    user.last_checkin = timezone.now() - timezone.timedelta(days=user.days_to_release_setting + 1)
    assert user.release_entries


class TestUser(TestCase):
    def setUp(self):
        self.user = UserFactory()
