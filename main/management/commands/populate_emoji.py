import pandas as pd
import base64
from django.core.management.base import BaseCommand
from main.models import Emoji

class Command(BaseCommand):
    help = 'Populates the Emoji model with data from a specified CSV file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_path',
            type=str,
            help='Path to the CSV file containing emoji data',
            default='/mnt/data/emoji_df.csv'  # Default path if none is provided
        )

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_path']  # Get the CSV path from arguments

        # Load the CSV data
        try:
            emoji_df = pd.read_csv(csv_file_path)
            self.stdout.write(self.style.SUCCESS(f"Loaded data from {csv_file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to load CSV file: {e}"))
            return

        # Iterate over DataFrame rows and populate the Emoji model
        for _, row in emoji_df.iterrows():
            encoded_emoji = base64.b64encode(row['emoji'].encode('utf-8')).decode('utf-8')
            Emoji.objects.create(
                emoji=encoded_emoji,
                name=row['name'],
                group=row['group'],
                sub_group=row['sub_group'],
                codepoints=row['codepoints']
            )

        self.stdout.write(self.style.SUCCESS("Emoji model populated successfully."))
