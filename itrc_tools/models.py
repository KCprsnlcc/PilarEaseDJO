# itrc_tools/models.py

from django.db import models
from django.conf import settings

class VerificationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verification_request')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True, null=True)  # Optional remarks

    def __str__(self):
        return f"VerificationRequest({self.user.username} - {self.status})"

class EnrollmentMasterlist(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    academic_year_level = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    # Add other fields as necessary

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"

# itrc_tools/models.py

class SystemSetting(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('verify', 'Verify User'),
        ('reject', 'Reject User'),
        ('upload_masterlist', 'Upload Masterlist'),
        # Add more actions as needed
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)  # Optional details

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"
