# Generated by Django 5.0.6 on 2024-08-01 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_remove_status_neutral'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='neutral',
            field=models.FloatField(default=0),
        ),
    ]