from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "journal_app.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import journal_app.users.signals  # noqa F401
        except ImportError:
            pass
