import pytest
from django.conf import settings
from django.test import TestCase, Client

pytestmark = pytest.mark.django_db


class TestSettings(TestCase):
    def test_settings(self):
        self.assertEqual(settings.TESTING, True)
