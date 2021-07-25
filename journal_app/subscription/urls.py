from django.conf import settings
from django.urls import path

from journal_app.subscription import views

app_name = "subscription"

urlpatterns = [
    path('', views.home, name='home'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('create-customer-portal-session/', views.create_stripe_portal_session, name='customer_portal'),
    path(settings.WEBHOOK_URL, views.stripe_webhook, name='webhook'),
]
