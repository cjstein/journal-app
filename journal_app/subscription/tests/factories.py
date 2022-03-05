import datetime
import string

from factory import SubFactory, fuzzy
from factory.django import DjangoModelFactory

from journal_app.subscription.models import StripeCustomer
from journal_app.users.tests.factories import UserFactory


def create_active_subscriber(user, **kwargs):
    customer = StripeCustomer.objects.get(user=user)
    customer.stripe_customer_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='cus_')
    customer.stripe_subscription_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='sub_')
    customer.product = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='prod_')
    customer.status = StripeCustomer.Status.ACTIVE
    customer.subscription_start = datetime.date(datetime.date.today().year, 1, 1)
    customer.subscription_end = customer.subscription_start + datetime.timedelta(days=365)
    customer.save()
    return customer


def create_trial_subscriber(user, **kwargs):
    customer = StripeCustomer.objects.get(user=user)
    customer.status = StripeCustomer.Status.TRIAL
    customer.trial_end = datetime.date.today() + datetime.timedelta(days=14)
    customer.save()
    return customer


def create_cancelled_subscriber(user, **kwargs):
    customer = StripeCustomer.objects.get(user=user)
    customer.stripe_customer_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='cus_')
    customer.stripe_subscription_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='sub_')
    customer.product = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='prod_')
    customer.status = StripeCustomer.Status.CANCELLED
    customer.subscription_start = datetime.date(datetime.date.today().year - 1, 1, 1)
    customer.subscription_end = customer.subscription_start + datetime.timedelta(days=365)
    customer.save()
    return customer
