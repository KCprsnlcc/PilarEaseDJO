# itrc_tools/models.py

from django.db import models
from django.conf import settings

class VerificationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='verification_request'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"VerificationRequest({self.user.username}) - {self.status}"

class EnrollmentMasterlist(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    academic_year_level = models.CharField(max_length=20)
    # Removed contact_number and email fields

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"

class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('verify', 'Verify User'),
        ('reject', 'Reject User'),
        ('upload_masterlist', 'Upload Masterlist'),
        ('update_setting', 'Update Setting'),
        ('create_setting', 'Create Setting'),
        ('delete_user', 'Delete User'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    details = models.TextField(default="Details not provided")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AuditLog({self.user.username} - {self.action} at {self.timestamp})"

class AuditLogEntry(models.Model):
    audit_log = models.ForeignKey(
        AuditLog,
        on_delete=models.CASCADE,
        related_name='entries'
    )
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entry for {self.audit_log} at {self.timestamp}"
