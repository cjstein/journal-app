from django.contrib import admin

from journal_app.journal_mail.models import Mail


@admin.register(Mail)
class MailItem(admin.ModelAdmin):
    list_display = (
        'to',
        'template_name',
        'datetime',
    )

    sortable_by = (
        'to',
        'template_name',
        'datetime',
    )

    search_fields = (
        'user',
        'to',
        'template_name',
    )

    list_filter = (
        'user',
        'template_name',
    )
