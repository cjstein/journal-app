import pytest
from django.contrib.auth.models import AnonymousUser
from django.http.response import Http404
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from journal_app.users.models import User
from journal_app.users.tests.factories import UserFactory
from journal_app.users.views import (
    UserRedirectView,
    UserUpdateView,
    anon_user_checkin_view,
    user_checkin_view,
    user_detail_view,
)

pytestmark = pytest.mark.django_db
REFERENCE_DATE = timezone.datetime(year=2019, month=10, day=30)


class TestUserUpdateView:

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()

        response = user_detail_view(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()  # type: ignore

        response = user_detail_view(request, username=user.username)

        assert response.status_code == 302
        assert response.url == "/accounts/login/?next=/fake-url/"

    def test_case_sensitivity(self, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory(username="UserName")

        with pytest.raises(Http404):
            user_detail_view(request, username="username")


class TestUserCheckinView(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1.last_checkin = REFERENCE_DATE
        self.user1.save()
        self.user2 = UserFactory()
        self.user2.last_checkin = REFERENCE_DATE
        self.user2.save()

    def test_checkin(self):
        # Every test needs access to the request factory
        self.client = Client()
        self.client.force_login(user=self.user1)
        assert self.user1.last_checkin == timezone.datetime(year=2019, month=10, day=30)
        response = self.client.get(
            reverse('users:checkin', kwargs={'username': self.user1.username}),
            follow=True,
        )
        self.assertRedirects(response,
                             reverse('journal:entry_list'),
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)
        self.user1.refresh_from_db()
        assert self.user1.last_checkin != REFERENCE_DATE

    def test_anon_checkin(self):
        self.client = Client()
        assert self.user2.last_checkin == timezone.datetime(year=2019, month=10, day=30)
        response = self.client.get(
            reverse('users:anon_checkin', kwargs={'username': self.user2.username, 'uuid': self.user2.checkin_link}),
            follow=True,
        )
        self.assertRedirects(response,
                             reverse('home'),
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)
