from django.contrib import admin

from journal_app.journal.models import Contact, Entry

# Register your models here.
admin.site.register(Entry)
admin.site.register(Contact)
