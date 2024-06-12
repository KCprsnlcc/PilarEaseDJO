# myapp/management/commands/hashcss.py
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from hash_css import process_css_files

class Command(BaseCommand):
    help = 'Generate hash for CSS files and rename them'

    def handle(self, *args, **kwargs):
        css_file_paths = [
            os.path.join(settings.BASE_DIR, 'static/css/style1.css'),  # Update this path
            os.path.join(settings.BASE_DIR, 'static/css/style2.css')   # Update this path
        ]
        new_file_names = process_css_files(css_file_paths)
        self.stdout.write(self.style.SUCCESS(f'New CSS file names: {new_file_names}'))
