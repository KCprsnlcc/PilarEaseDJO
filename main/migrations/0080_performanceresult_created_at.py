# Generated by Django 5.0.6 on 2024-11-05 13:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0079_dataset_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='performanceresult',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]