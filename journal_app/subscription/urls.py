from django.urls import path
from journal_app.subscription import views


app_name = "subscription"

urlpatterns = [
    path('', views.home, name='home'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.success),
    path('cancel/', views.cancel),
    path('webhook/', views.stripe_webhook),
]
