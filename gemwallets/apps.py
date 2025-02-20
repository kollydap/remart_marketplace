from django.apps import AppConfig


class GemwalletsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gemwallets"

    def ready(self):
        import gemwallets.signals
