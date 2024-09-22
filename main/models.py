from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    student_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    academic_year_level = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)  
    is_counselor = models.BooleanField(default=False)
    block_reason = models.CharField(max_length=255, blank=True, null=True)
    block_duration = models.IntegerField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.full_name or self.username   
    
class EmailHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_history')
    email = models.EmailField()
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} for {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True) 
    is_email_verified = models.BooleanField(default=False)
    new_email = models.EmailField(blank=True, null=True)
    email_change_requested_at = models.DateTimeField(null=True, blank=True)  # Track when email change was requested
    email_verification_requested_at = models.DateTimeField(null=True, blank=True)  # Track when email verification was requested
    
    def __str__(self):
        return self.user.username
    
CustomUser = get_user_model()

User = get_user_model()

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sentiment_score = models.FloatField(default=0.0)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"
    
class ChatSession(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"ChatSession for {self.user.username} at {self.created_at}"

class Questionnaire(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(default='No answer provided')
    response = models.TextField(default='No response provided')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question: {self.question[:50]}... - User: {self.user.username}"

class Status(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    plain_description = models.TextField()
    emotion = models.CharField(max_length=50)
    anger = models.FloatField(default=0)
    disgust = models.FloatField(default=0)
    fear = models.FloatField(default=0)
    neutral = models.FloatField(default=0)
    happiness = models.FloatField(default=0)
    sadness = models.FloatField(default=0)
    surprise = models.FloatField(default=0)
    anger_percentage = models.IntegerField(default=0)
    disgust_percentage = models.IntegerField(default=0)
    fear_percentage = models.IntegerField(default=0)
    neutral_percentage = models.IntegerField(default=0)
    happiness_percentage = models.IntegerField(default=0)
    sadness_percentage = models.IntegerField(default=0)
    surprise_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='notifications', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Status: {self.status.title}"

class ReplyNotification(Notification):
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_notifications')

    def __str__(self):
        return f"{self.replied_by.username} replied to {self.status.title}"
    
class UserNotificationSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    has_clicked_notification = models.BooleanField(default=False)  # Track if user clicked the notification button

class Referral(models.Model):
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    referred_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    highlighted_title = models.TextField(blank=True)
    highlighted_description = models.TextField(blank=True)
    referral_reason = models.CharField(max_length=255, default='Not specified')  # Define a default value here
    other_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral by {self.referred_by.username} for {self.status.title}"

    
class Reply(models.Model):
    status = models.ForeignKey('Status', related_name='replies', on_delete=models.CASCADE)
    parent_reply = models.ForeignKey('self', related_name='nested_replies', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.status.title}"

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
 

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_notification_settings(sender, instance, created, **kwargs):
    if created:
        UserNotificationSettings.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()