from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'art_project.accounts'

    def ready(self):
        import art_project.accounts.signals
