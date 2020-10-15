from django.apps import AppConfig


class JournalConfig(AppConfig):
    name = 'journal_app.journal'
    verbose_name = "Journal"

    def ready(self):
        try:
            import journal_app.journal.signals  # noqa F401
        except ImportError:
            pass
