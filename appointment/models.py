from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

class AppointmentSchedule(models.Model):
    """Model for storing available appointment slots"""
    counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='available_schedules',
        limit_choices_to={'is_counselor': True}
    )
    date = models.DateField()
    day_of_week = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    ], null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        verbose_name = 'Appointment Schedule'
        verbose_name_plural = 'Appointment Schedules'
        
    def __str__(self):
        return f"{self.counselor.full_name} - {self.date} ({self.start_time} to {self.end_time})"
    
    def clean(self):
        # Ensure start_time is before end_time
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            from django.core.exceptions import ValidationError
            raise ValidationError("Start time must be before end time")
            
class AppointmentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    CANCELLED = 'cancelled', 'Cancelled'
    COMPLETED = 'completed', 'Completed'
    RESCHEDULED = 'rescheduled', 'Rescheduled'
    NO_SHOW = 'no_show', 'No Show'

class Appointment(models.Model):
    """Model for appointment bookings"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_appointments'
    )
    counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='counselor_appointments',
        limit_choices_to={'is_counselor': True}
    )
    schedule = models.ForeignKey(
        AppointmentSchedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING
    )
    counselor_notes = models.TextField(blank=True, null=True)
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', 'start_time']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        
    def __str__(self):
        return f"{self.user.full_name} with {self.counselor.full_name} on {self.date}"
    
    @property
    def is_past(self):
        return self.date < timezone.now().date() or (
            self.date == timezone.now().date() and 
            self.end_time < timezone.now().time()
        )
    
    @property
    def can_be_cancelled(self):
        return self.status in [AppointmentStatus.PENDING, AppointmentStatus.APPROVED]
        
class AppointmentNotification(models.Model):
    """Model for notifications related to appointments"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointment_notifications'
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Appointment Notification'
        verbose_name_plural = 'Appointment Notifications'
    
    def __str__(self):
        return f"Notification for {self.user.username} about {self.appointment}"

class AppointmentReport(models.Model):
    """Model for storing generated appointment reports"""
    REPORT_TYPES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom')
    ]
    
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='generated_reports'
    )
    data = models.JSONField(default=dict)
    file = models.FileField(upload_to='appointment_reports/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Appointment Report'
        verbose_name_plural = 'Appointment Reports'
        
    def __str__(self):
        return f"{self.title} ({self.start_date} to {self.end_date})"

class BlockedTimeSlot(models.Model):
    """Model for blocking specific time slots"""
    counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocked_slots',
        limit_choices_to={'is_counselor': True}
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        verbose_name = 'Blocked Time Slot'
        verbose_name_plural = 'Blocked Time Slots'
        
    def __str__(self):
        return f"{self.counselor.full_name} - {self.date} ({self.start_time} to {self.end_time})"
