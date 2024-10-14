# itrc_tools/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from main.models import CustomUser, Feedback
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

class APIPerformanceLog(models.Model):
    endpoint = models.CharField(max_length=255)
    response_time = models.FloatField(help_text="Response time in milliseconds")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.endpoint} - {self.response_time}ms at {self.timestamp}"

class ErrorLog(models.Model):
    ERROR_TYPE_CHOICES = [
        ('500', 'Server Error'),
        ('404', 'Not Found'),
        ('403', 'Forbidden'),
        ('400', 'Bad Request'),
        ('401', 'Unauthorized'),
        # Add more as needed
    ]

    error_type = models.CharField(max_length=10, choices=ERROR_TYPE_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.error_type} at {self.endpoint} on {self.timestamp}"
    
    # itrc_tools/models.py

class SystemDowntime(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Downtime from {self.start_time} to {self.end_time} - Reason: {self.reason}"

# itrc_tools/models.py

class PageViewLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='page_views')
    page = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} viewed {self.page} at {self.timestamp}"

# itrc_tools/models.py

class FeatureUtilizationLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feature_utilizations')
    feature_name = models.CharField(max_length=255)
    usage_count = models.IntegerField(default=0)
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} used {self.feature_name} {self.usage_count} times"


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

CustomUser = get_user_model()
# itrc_tools/models.py

class SessionLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='session_logs')
    session_start = models.DateTimeField()
    session_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session for {self.user.username} from {self.session_start} to {self.session_end}"
