from django.contrib import admin

from journal_app.subscription.models import StripeCustomer, Subscription


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'stripe_customer_id',
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


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'price_unit',
        'stripe_price_id',
        'uuid',
    ]

    sortable_by = [
        'name',
        'price',
    ]

    list_filter = [
        'price_unit',
    ]

    readonly_fields = ['uuid']
