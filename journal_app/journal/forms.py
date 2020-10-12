from django.forms import ModelForm, CharField, ValidationError
from tinymce.widgets import TinyMCE
from .models import Entry, Contact


class EntryForm(ModelForm):

    class Meta:
        model = Entry
        fields = ['title', 'body']
        widgets = {
            'body': TinyMCE(attrs={'cols': 80, 'rows': 10, 'id': 'tinymceid'}),
        }


class ContactForm(ModelForm):

    def clean(self):
        clean_data = super().clean()
        email = clean_data.get('email')
        phone = clean_data.get('phone')
        password = clean_data.get('password')
        if not email and not password and not phone:
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
