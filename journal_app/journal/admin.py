from django.contrib import admin
from journal_app.journal.models import Entry, Contact

# Register your models here.
admin.site.register(Entry)
admin.site.register(Contact)
