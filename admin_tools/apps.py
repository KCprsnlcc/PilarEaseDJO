from django.apps import AppConfig

class AdminToolsConfig(AppConfig):
    name = 'admin_tools'

    def ready(self):
        # Import signals to connect the post_migrate handler
        import admin_tools.signals  # noqa
