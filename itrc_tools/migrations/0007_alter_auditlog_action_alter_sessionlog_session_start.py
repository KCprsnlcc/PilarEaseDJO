# Generated by Django 5.0.6 on 2024-10-15 11:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itrc_tools', '0006_apiperformancelog_errorlog_systemdowntime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditlog',
            name='action',
            field=models.CharField(choices=[('verify', 'Verify User'), ('reject', 'Reject User'), ('upload_masterlist', 'Upload Masterlist'), ('update_setting', 'Update Setting'), ('create_setting', 'Create Setting'), ('delete_user', 'Delete User'), ('register', 'User Registration'), ('login', 'User Login'), ('logout', 'User Logout')], max_length=50),
        ),
        migrations.AlterField(
            model_name='sessionlog',
            name='session_start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]