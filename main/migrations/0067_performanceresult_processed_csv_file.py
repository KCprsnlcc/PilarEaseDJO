# Generated by Django 5.0.6 on 2024-10-18 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0066_dataset_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='performanceresult',
            name='processed_csv_file',
            field=models.FileField(blank=True, null=True, upload_to='processed_datasets/'),
        ),
    ]
