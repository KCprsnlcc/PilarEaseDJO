# Generated by Django 5.0.6 on 2024-07-01 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='read',
            new_name='is_read',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='url',
            new_name='link',
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(),
        ),
    ]
