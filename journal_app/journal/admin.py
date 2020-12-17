from django.contrib import admin

from journal_app.journal.models import Contact, Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'created',
        'released',
    )

    sortable_by = (
        'user',
        'created',
    )

    search_fields = (
        'title',
        'uuid',
        'user',
        'contact',
    )

    list_filter = (
        'user',
        'released',
        'public',
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'uuid',
        'email',
        'phone',
    )

    sortable_by = (
        'name',
    )

    search_fields = (
        'uuid',
        'user',
        'name',
        'email',
        'phone'
    )

    list_filter = (
        'user',
    )
