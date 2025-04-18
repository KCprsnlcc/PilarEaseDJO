# itrc_tools/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from main.models import CustomUser, Feedback
from django.utils import timezone
from django.db import transaction
class VerificationRequest(models.Model):
        # Define the choices somewhere
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('auto_accepted', 'Auto Accepted'),
        ('auto_rejected', 'Auto Rejected'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)



    def auto_accept(self):
        with transaction.atomic():
            self.status = 'auto_accepted'
            self.remarks = 'Automatically accepted by system.'
            self.save()

            user = self.user
            user.is_active = True
            user.is_verified = True
            user.verification_status = 'verified'
            user.save()

    def auto_reject(self):
        with transaction.atomic():
            self.status = 'auto_rejected'
            self.remarks = 'Automatically rejected by system.'
            self.save()

            user = self.user
            user.is_active = False
            user.is_verified = False
            user.verification_status = 'rejected'
            user.save()
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
    value = models.CharField(max_length=100)
    auto_accept_enabled = models.BooleanField(default=False)
    auto_reject_enabled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @staticmethod
    def set_setting(key, value):
        setting, created = SystemSetting.objects.update_or_create(
            key=key,
            defaults={'value': value}
        )
        return setting

    @staticmethod
    def get_setting(key, default=None):
        try:
            return SystemSetting.objects.get(key=key).value
        except SystemSetting.DoesNotExist:
            return default
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('verify', 'Verify User'),
        ('reject', 'Reject User'),
        ('upload_masterlist', 'Upload Masterlist'),
        ('update_setting', 'Update Setting'),
        ('create_setting', 'Create Setting'),
        ('delete_user', 'Delete User'),
        ('register', 'User Registration'),    # New Action
        ('login', 'User Login'),              # New Action
        ('logout', 'User Logout'),            # New Action
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES
    )
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='session_logs'
    )
    session_start = models.DateTimeField(default=timezone.now)
    session_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session for {self.user.username} started at {self.session_start}"

class SessionLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


class Notification_System(models.Model):
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='itrc_notifications'
    )
    notification_type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES,
        default='info'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)  # Optional link to related content

    def __str__(self):
        return f"Notification({self.notification_type}) for {self.user.username} at {self.timestamp}"
