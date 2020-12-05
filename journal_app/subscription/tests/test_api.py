# Standard library imports
from unittest.mock import Mock, patch

# 3rd party imports
import stripe
from nose.tools import assert_is_none


SUBSCRIPTION = {
    "id": "sub_IMW8JDBaFcu3tH",
    "object": "subscription",
    "application_fee_percent": None,
    "billing_cycle_anchor": 1604977255,
    "billing_thresholds": None,
    "cancel_at": None,
    "cancel_at_period_end": False,
    "canceled_at": 1605058103,
    "collection_method": "charge_automatically",
    "created": 1604977255,
    "current_period_end": 1636513255,
    "current_period_start": 1604977255,
    "customer": "cus_INVFtrGTytd9FO",
    "days_until_due": None,
    "default_payment_method": "pm_1Hln6IEAWjMWH1XhQIdfAm8V",
    "default_source": None,
    "default_tax_rates": [],
    "discount": None,
    "ended_at": 1605058103,
    "items": {
        "object": "list",
        "data": [
            {
                "id": "si_IMW8UzhxCPsKVj",
                "object": "subscription_item",
                "billing_thresholds": None,
                "created": 1604977256,
                "metadata": {},
                "price": {
                    "id": "price_1HllJdEAWjMWH1XhgdHYhQ5g",
                    "object": "price",
                    "active": True,
                    "billing_scheme": "per_unit",
                    "created": 1604970393,
                    "currency": "usd",
                    "livemode": False,
                    "lookup_key": None,
                    "metadata": {},
                    "nickname": None,
                    "product": "prod_IMUIWW5d3yX5QD",
                    "recurring": {
                        "aggregate_usage": None,
                        "interval": "year",
                        "interval_count": 1,
                        "usage_type": "licensed"
                    },
                    "tiers_mode": None,
                    "transform_quantity": None,
                    "type": "recurring",
                    "unit_amount": 3000,
                    "unit_amount_decimal": "3000"
                },
                "quantity": 1,
                "subscription": "sub_IMW8JDBaFcu3tH",
                "tax_rates": []
            }
        ],
        "has_more": False,
        "url": "/v1/subscription_items?subscription=sub_IMW8JDBaFcu3tH"
    },
    "latest_invoice": "in_1Hln6JEAWjMWH1Xhj5GnVrnw",
    "livemode": False,
    "metadata": {},
    "next_pending_invoice_item_invoice": None,
    "pause_collection": None,
    "pending_invoice_item_interval": None,
    "pending_setup_intent": None,
    "pending_update": None,
    "schedule": None,
    "start_date": 1604977255,
    "status": "canceled",
    "transfer_data": None,
    "trial_end": None,
    "trial_start": None
}


CUSTOMER = {
    "id": "cus_INVFtrGTytd9FO",
    "object": "customer",
    "address": None,
    "balance": 0,
    "created": 1605204601,
    "currency": "usd",
    "default_source": None,
    "delinquent": False,
    "description": "My First Test Customer (created for API docs)",
    "discount": None,
    "email": "bobbelderbos@gmail.com",
    "invoice_prefix": "61C889F1",
    "invoice_settings": {
        "custom_fields": None,
        "default_payment_method": None,
        "footer": None
    },
    "livemode": False,
    "metadata": {},
    "name": None,
    "next_invoice_sequence": 2,
    "phone": None,
    "preferred_locales": [],
    "shipping": None,
    "tax_exempt": "none"
}


@patch('stripe.Subscription.retrieve')
def test_retrieve_subscription(mock_retrieve):
       mock_retrieve.return_value.json.return_value = SUBSCRIPTION


@patch('stripe.Subscription.create')
def test_create_subscription(mock_create):
    mock_create.return_value.json.return_value = SUBSCRIPTION


@patch('stripe.Customer.create')
def test_create_customer(mock_create):
    mock_create.return_value.json.return_value = CUSTOMER


@patch('stripe.Customer.retrieve')
def test_create_retrieve(mock_create):
    mock_create.return_value.json.return_value = CUSTOMER
