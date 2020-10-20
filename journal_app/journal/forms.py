from django.forms import ModelForm, ValidationError, CheckboxSelectMultiple
from tinymce.widgets import TinyMCE
from journal_app.journal.models import Entry, Contact


class EntryForm(ModelForm):

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
            'contact': CheckboxSelectMultiple,
        }
        labels = {
            'public': 'Release everyone on your contact list?',
            'contact': 'Share with:',
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
