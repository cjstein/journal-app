from django.forms import ModelForm, ValidationError
from tinymce.widgets import TinyMCE
from .models import Entry, Contact


class EntryForm(ModelForm):

    class Meta:
        model = Entry
        fields = ['title', 'body']
        widgets = {
            'body': TinyMCE(attrs={'id': 'tinymceid'}),
        }


class ContactForm(ModelForm):

    def clean(self):
        clean_data = super().clean()
        email = clean_data.get('email')
        phone = clean_data.get('phone')
        password = clean_data.get('password')
        if not any([email, password, phone]):
            raise ValidationError(
                {
                    'email': 'At least one of Email, Password or Phone needs to filled',
                    'phone': 'At least one of Email, Password or Phone needs to filled',
                    'password': 'At least one of Email, Password or Phone needs to filled',
                }
            )

    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'phone',
            'password',
        ]
