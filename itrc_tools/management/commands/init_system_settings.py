# itrc_tools/management/commands/init_system_settings.py

from django.core.management.base import BaseCommand
from itrc_tools.models import SystemSetting

class Command(BaseCommand):
    help = 'Initialize system settings for ITRC Tools'

    def handle(self, *args, **kwargs):
        settings = {
            'auto_accept_enabled': 'false',
            'auto_reject_enabled': 'false',
        }
        for key, value in settings.items():
            SystemSetting.set_setting(key, value)
            self.stdout.write(self.style.SUCCESS(f'Set {key} to {value}'))

        self.stdout.write(self.style.SUCCESS('System settings initialized successfully.'))
