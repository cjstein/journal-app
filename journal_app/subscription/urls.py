from django.urls import path
from journal_app.subscription.views import home, stripe_config, create_checkout_session, success, cancel


app_name = "subscription"

urlpatterns = [
    path('', home, name='home'),
    path('config/', stripe_config),
    path('create-checkout-session/', create_checkout_session),
    path('success/', success),  # new
    path('cancel/', cancel),
]
