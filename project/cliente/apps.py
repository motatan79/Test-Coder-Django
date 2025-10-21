from django.apps import AppConfig


class ClienteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cliente"

    def ready(self):
        # Import signals to ensure Perfil is created for new users
        try:
            import cliente.signals  # noqa: F401
        except Exception:
            pass
