from django.utils import timezone
from factory import SubFactory
from factory.django import DjangoModelFactory

from journal_app.subscription.models import StripeCustomer
from journal_app.users.tests.factories import UserFactory


class ActiveSubscriber(DjangoModelFactory):
    user = SubFactory(UserFactory)
    status = StripeCustomer.Status.ACTIVE

    class Meta:
        model = StripeCustomer


class TrialSubscriber(DjangoModelFactory):
    user = SubFactory(UserFactory)
    status = StripeCustomer.Status.TRIAL
    trial_end = timezone.now() + timezone.timedelta(days=14)

    class Meta:
        model = StripeCustomer


class ExpiredSubscriber(DjangoModelFactory):
    user = SubFactory(UserFactory)
    status = StripeCustomer.Status.CANCELLED

    class Meta:
        model = StripeCustomer
