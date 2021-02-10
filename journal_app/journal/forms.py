from dal import autocomplete
from django import forms
from django.forms import ModelForm, ValidationError
from django.utils import timezone
from tinymce.widgets import TinyMCE

from journal_app.journal.models import Contact, Entry


class DateInput(forms.DateInput):
    input_type = 'text'


class EntryForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['contact'].queryset = Contact.objects.filter(user=user)

    class Meta:
        model = Entry
        fields = [
            'title',
            'public',
            'body',
            'contact',
        ]
        widgets = {
            'body': TinyMCE(attrs={'id': 'tinymceid'}),
            'contact': autocomplete.ModelSelect2Multiple(url='journal:contact-autocomplete'),
        }
        labels = {
            'public': 'Release everyone on your contact list?',
            'contact': 'Share with:',
        }


class EntryScheduleForm(ModelForm):

    def clean(self):
        clean_data = super().clean()
        date = clean_data['scheduled_time']
        if date <= timezone.now().date():
            raise ValidationError({
                'scheduled_time': 'Scheduled time has to be in the future',
            })

    class Meta:
        model = Entry
        fields = ['scheduled_time']
        widgets = {
            'scheduled_time': DateInput(),
        }


class ContactForm(ModelForm):

    def clean(self):
        clean_data = super().clean()
        email = clean_data.get('email')
        phone = clean_data.get('phone')
        if not any([email, phone]):
            raise ValidationError(
                {
                    'email': 'At least one of Email or Phone needs to filled',
                    'phone': 'At least one of Email or Phone needs to filled',
                }
            )

    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'phone',
        ]
        labels = {
            'phone': 'Phone Number: (Only works for US numbers)'
        }


class EntryContactAddForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(EntryContactAddForm, self).__init__(*args, **kwargs)
        self.fields['contact'].queryset = Contact.objects.filter(user=user)

    class Meta:
        model = Entry
        fields = [
            'contact'
        ]
        widgets = {
            'contact': autocomplete.ModelSelect2Multiple(url='journal:contact-autocomplete'),
        }
