from django.forms import ModelForm, CharField
from tinymce.widgets import TinyMCE
from .models import Entry


class EntryForm(ModelForm):

    body = CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Entry
        fields = ['title', 'body']
        widgets = {
            'body': TinyMCE(attrs={'cols': 80, 'rows': 10, 'id': 'tinymceid'}),
        }
