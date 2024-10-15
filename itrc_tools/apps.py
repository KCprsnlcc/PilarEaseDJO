# itrc_tools/apps.py

from django.apps import AppConfig

class ItrcToolsConfig(AppConfig):
    name = 'itrc_tools'

    def ready(self):
        import itrc_tools.signals  # Import signals to register them
