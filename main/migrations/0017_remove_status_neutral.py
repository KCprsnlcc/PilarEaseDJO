# Generated by Django 5.0.6 on 2024-08-01 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_status_neutral'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='neutral',
        ),
    ]