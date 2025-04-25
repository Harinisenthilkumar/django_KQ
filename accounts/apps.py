from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from django.contrib.auth.signals import user_logged_in
        from django.contrib.auth.models import update_last_login

        # This disconnects the signal that tries to update last_login
        user_logged_in.disconnect(update_last_login)