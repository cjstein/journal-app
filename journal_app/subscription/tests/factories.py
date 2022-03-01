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


def create_active_subscriber(user, **kwargs):
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
    return StripeCustomer.objects.create(
        user=user,
        stripe_customer_id=stripe_customer_id,
        stripe_subscription_id=stripe_subscription_id,
        product=product,
        status=status,
        subscription_start=subscription_start,
        subscription_end=subscription_end,
        **kwargs
    )


class TrialSubscriberFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    stripe_customer_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters+string.digits, prefix='cus_')
    # stripe_subscription_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters+string.digits, prefix='sub_')
    product = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='prod_')
    status = StripeCustomer.Status.TRIAL
    trial_end = datetime.date.today() + datetime.timedelta(days=14)

    class Meta:
        model = StripeCustomer


def create_trial_subscriber(user, **kwargs):
    stripe_customer_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='cus_')
    stripe_subscription_id = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='sub_')
    product = fuzzy.FuzzyText(length=18, chars=string.ascii_letters + string.digits, prefix='prod_')
    status = StripeCustomer.Status.TRIAL
    trial_end = datetime.date.today() + datetime.timedelta(days=14)
    return StripeCustomer.objects.create(
        user=user,
        stripe_customer_id=stripe_customer_id,
        stripe_subscription_id=stripe_subscription_id,
        product=product,
        status=status,
        trial_end=trial_end,
        **kwargs
    )


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
