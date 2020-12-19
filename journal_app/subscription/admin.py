from django.contrib import admin

from journal_app.subscription.models import StripeCustomer


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'status',
        'subscription_end',
    ]

    sortable_by = [
        'user',
        'subscription_end',
    ]

    list_filter = [
        'product_name',
        'status',
    ]

    search_fields = [
        'user',
        'product_name',
        'stripe_customer_id',
        'stripe_subscription_id',
    ]
