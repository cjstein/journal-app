from django.apps import AppConfig


class JournalMailConfig(AppConfig):
    name = 'journal_app.journal_mail'

    def ready(self):
        import signals
