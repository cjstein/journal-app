from django.db import models
from journal_app.journal.models import Contact


def test_user_owns(request, model: models.Model, pk):
    # This tests whether the user owns the model
    test_model = model.objects.get(pk=pk)
    return request.user == test_model.user


def test_user_has_subscription(request):
    # This test whether the User has an active or trial Subscription
    subscription_valid = (
        request.user.subscription.status == 'trialing' or
        request.user.subscription.status == 'active'
    )
    return subscription_valid


def get_entries_from_contact(pk):
    context = {}
    contact = Contact.objects.get(pk=pk)
    entry_list = contact.entry_set.all()
    context['contact'] = contact
    context['entries'] = entry_list
    return context
