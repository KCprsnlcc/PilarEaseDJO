# Generated by Django 5.0.6 on 2024-09-18 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_remove_reply_parent_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='parent_reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nested_replies', to='main.reply'),
        ),
    ]
