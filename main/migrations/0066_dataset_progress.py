# Generated by Django 5.0.6 on 2024-10-18 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0065_alter_dataset_csv_file_alter_dataset_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='progress',
            field=models.JSONField(default=dict),
        ),
    ]