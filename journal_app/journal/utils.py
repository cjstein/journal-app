from django.db import models
from journal_app.journal.models import Contact


def test_user_owns(request, model: models.Model, pk):
    test_model = model.objects.get(pk=pk)
    return request.user == test_model.user


def get_entries_from_contact(request, pk):
    context = {}
    contact = Contact.objects.get(user=request.user, pk=pk)
    entry_list = contact.entry_set.all()
    context['contact'] = contact
    context['entry_list'] = entry_list
    return context
