# Generated by Django 5.0.6 on 2024-10-29 06:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itrc_tools', '0013_alter_verificationrequest_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsetting',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='systemsetting',
            name='value',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='verificationrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected'), ('auto_accepted', 'Auto Accepted'), ('auto_rejected', 'Auto Rejected')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='verificationrequest',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]