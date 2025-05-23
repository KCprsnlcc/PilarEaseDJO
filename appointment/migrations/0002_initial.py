# Generated by Django 4.2.21 on 2025-05-15 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockedtimeslot',
            name='counselor',
            field=models.ForeignKey(limit_choices_to={'is_counselor': True}, on_delete=django.db.models.deletion.CASCADE, related_name='blocked_slots', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentschedule',
            name='counselor',
            field=models.ForeignKey(limit_choices_to={'is_counselor': True}, on_delete=django.db.models.deletion.CASCADE, related_name='available_schedules', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentreport',
            name='generated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='generated_reports', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentnotification',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='appointment.appointment'),
        ),
        migrations.AddField(
            model_name='appointmentnotification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='counselor',
            field=models.ForeignKey(limit_choices_to={'is_counselor': True}, on_delete=django.db.models.deletion.CASCADE, related_name='counselor_appointments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='appointment.appointmentschedule'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_appointments', to=settings.AUTH_USER_MODEL),
        ),
    ]
