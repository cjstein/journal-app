from django.contrib import admin

from journal_app.subscription.models import StripeCustomer

admin.site.register(StripeCustomer)
