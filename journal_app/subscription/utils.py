import stripe
from django.conf import settings
from django.utils.timezone import datetime

from journal_app.subscription.models import StripeCustomer


def get_subscription_status(user):
    """
    This takes a user and returns their subscription information
    """
    # Retrieve the subscription & product
    stripe_customer = StripeCustomer.objects.get(user=user)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
    product = stripe.Product.retrieve(subscription.plan.product)
    subscription_end = datetime.fromtimestamp(subscription.current_period_end)
    return {
        'subscription': subscription,
        'product': product,
        'subscription_end': subscription_end,
    }

    # Feel free to fetch any additional data from 'subscription' or 'product'
    # https://stripe.com/docs/api/subscriptions/object
    # https://stripe.com/docs/api/products/object
