import datetime
import string

from factory import SubFactory, fuzzy
from factory.django import DjangoModelFactory

from journal_app.subscription.models import StripeCustomer
from journal_app.users.tests.factories import UserFactory

# I don't need these because an instance gets created at User creation based on the signal
# I'm leaving these here in case I change things


class ActiveSubscriberFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    stripe_customer_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='cus_')
    stripe_subscription_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='sub_')
    product = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='prod_')
    status = StripeCustomer.Status.ACTIVE
    subscription_start = fuzzy.FuzzyDate(
        start_date=datetime.date(datetime.date.today().year, 1, 1),
        end_date=datetime.date(datetime.date.today().year, 12, 31),
    )
    subscription_end = fuzzy.FuzzyDate(
        start_date=datetime.date.today(),
        end_date=datetime.date(datetime.date.today().year + 1, datetime.date.today().month, datetime.date.today().day)
    )

    class Meta:
        model = StripeCustomer


class TrialSubscriberFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    stripe_customer_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters+string.digits, prefix='cus_')
    # stripe_subscription_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters+string.digits, prefix='sub_')
    product = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='prod_')
    status = StripeCustomer.Status.TRIAL
    trial_end = datetime.date.today() + datetime.timedelta(days=14)

    class Meta:
        model = StripeCustomer


class ExpiredSubscriberFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    stripe_customer_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='cus_')
    stripe_subscription_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='sub_')
    product = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='prod_')
    status = StripeCustomer.Status.CANCELLED
    subscription_end = fuzzy.FuzzyDate(
        start_date=datetime.date(datetime.date.today().year, 1, 1),
        end_date=datetime.date.today(),
    )
    subscription_start = fuzzy.FuzzyDate(
        start_date=datetime.date(
            datetime.date.today().year - 2,
            datetime.date.today().month,
            datetime.date.today().day
        ),
        end_date=datetime.date(
            datetime.date.today().year - 1,
            datetime.date.today().month,
            datetime.date.today().day
        ),
    )

    class Meta:
        model = StripeCustomer
