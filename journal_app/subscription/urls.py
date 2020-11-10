from django.urls import path
from journal_app.subscription.views import home


app_name = "subscription"

urlpatterns = [
    path('', home, name='home'),
]
