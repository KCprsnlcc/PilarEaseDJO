# main/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from textblob import TextBlob  # Ensure TextBlob is installed: pip install textblob
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import BaseUserManager
import re
from django.core.validators import FileExtensionValidator
import uuid  # 
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, email, and password.
        """
        extra_fields.setdefault('is_itrc_staff', True)
        extra_fields.setdefault('student_id', self._get_next_student_id())

        return self.create_user(username, email, password, **extra_fields)

    def _get_next_student_id(self):
        # Fetch the last user, assuming student_id starts with a character followed by numbers (e.g., 'C665736').
        last_user = CustomUser.objects.filter(student_id__regex=r'^[A-Za-z]\d+$').order_by('student_id').last()

        if last_user:
            # Extract the numeric part of the student_id
            match = re.match(r'([A-Za-z]+)(\d+)', last_user.student_id)
            if match:
                prefix, number = match.groups()
                next_number = str(int(number) + 1).zfill(len(number))
                return f"{prefix}{next_number}"

        # Default for the first student_id if no users exist
        return "C000001"

class CustomUser(AbstractUser):
    # Removed `is_superuser` and `is_staff`
    student_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    academic_year_level = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_counselor = models.BooleanField(default=False)
    block_reason = models.CharField(max_length=255, blank=True, null=True)
    block_duration = models.IntegerField(blank=True, null=True)
    
    objects = CustomUserManager()

    # Custom field to identify ITRC staff
    is_itrc_staff = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('deactivated', 'Deactivated'),
    ]
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='pending'
    )

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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_history'
    )
    email = models.EmailField()
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} for {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    new_email = models.EmailField(blank=True, null=True)
    email_change_requested_at = models.DateTimeField(null=True, blank=True)
    email_verification_requested_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Feedback(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    message = models.TextField()
    sentiment_score = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    is_excluded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Excluded" if self.is_excluded else ("Approved" if self.is_approved else "Pending")
        return f"Feedback by {self.user.username} - {status}"

    def save(self, *args, **kwargs):
        blob = TextBlob(self.message)
        # Sentiment polarity ranges from -1 (negative) to 1 (positive). Normalize it to -100 to 100.
        normalized_score = blob.sentiment.polarity * 100
        self.sentiment_score = int(round(normalized_score))
        super().save(*args, **kwargs)
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ('greeting', 'Greeting'),
        ('question', 'Question'),
        ('bot_message', 'Bot Message'),
        ('user_message', 'User Message'),
        ('counselor_message', 'Counselor Message'),  # New Type
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_bot_message = models.BooleanField(default=False)
    message_type = models.CharField(max_length=50, choices=MESSAGE_TYPES, blank=True, null=True)
    question_index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.is_bot_message:
            sender = "Counselor" if self.message_type == 'counselor_message' else "Bot"
        else:
            sender = self.user.username
        return f"{sender}: {self.message[:50]}"

class QuestionnaireProgress(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_question_index = models.IntegerField(default=-1)  # -1 indicates questionnaire hasn't started
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Progress: {self.last_question_index}"
class NLTKResource(models.Model):
    name = models.CharField(
        default='No nltk downloaded',
        max_length=100,
        unique=True
    )
    is_downloaded = models.BooleanField(default=False)
    download_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Questionnaire(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    question = models.TextField()
    answer = models.TextField(default='No answer provided')
    response = models.TextField(default='No response provided')
    timestamp = models.DateTimeField(auto_now=True)  # Updated to auto_now to capture updates
    answer_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Changed to UUIDField

    class Meta:
        unique_together = ('user', 'question')  # Enforce uniqueness per user-question pair

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
    
class Dataset(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)  # Added this line
    csv_file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    error_log = models.TextField(blank=True, null=True)
    progress = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"Dataset {self.id} ({self.name}) uploaded by {self.user.username}"
    
class PerformanceResult(models.Model):
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE, related_name='performance_result')
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    confusion_matrix_image = models.TextField()  # Base64 encoded image
    classification_report_html = models.TextField()  # HTML table
    classification_report_csv = models.TextField()  # Base64 encoded CSV
    processed_csv_file = models.FileField(upload_to='processed_datasets/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)  # New field for timestamp

    def __str__(self):
        return f"Performance Result for Dataset {self.dataset.id}"

class TextAnalysis(models.Model):
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='text_analyses'
    )
    analysis_data = models.JSONField(blank=True, null=True)  # Using Django's built-in JSONField for JSONB storage

    def __str__(self):
        return f"Text Analysis {self.id} for Dataset {self.dataset.id}"
    
class NotificationCounselor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counselor_notifications')
    message = models.TextField()
    link = models.URLField(max_length=500, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(
        'Status',
        on_delete=models.CASCADE,
        related_name='counselor_notifications',  # Updated related_name to avoid conflicts
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.is_read else 'Unread'}"

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.ForeignKey(
        'Status',
        on_delete=models.CASCADE,
        related_name='notifications',
        blank=True,
        null=True
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.status:
            return f"Notification for {self.user.username} - Status: {self.status.title}"
        else:
            return f"Notification for {self.user.username}"

class ReplyNotification(Notification):
    replied_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reply_notifications'
    )

    def __str__(self):
        return f"{self.replied_by.username} replied to {self.status.title}"

class Emoji(models.Model):
    id = models.AutoField(primary_key=True)
    emoji = models.TextField(null=True)
    name = models.TextField(null=True)
    group = models.TextField(null=True)
    sub_group = models.TextField(null=True)
    codepoints = models.TextField(null=True)

    def __str__(self):
        return f"{self.emoji} - {self.name}"

    class Meta:
        ordering = ['sub_group']


class UserNotificationSettings(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )
    has_clicked_notification = models.BooleanField(default=False)

class Referral(models.Model):
    status = models.ForeignKey(
        'Status',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    referred_by = models.ForeignKey(
        CustomUser,  # Directly referencing the CustomUser model
        on_delete=models.CASCADE,
        related_name='referrals'  # Optional: allows reverse querying from CustomUser to referrals
    )
    highlighted_title = models.TextField(blank=True)
    highlighted_description = models.TextField(blank=True)
    referral_reason = models.CharField(
        max_length=255,
        default='Not specified'
    )
    other_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.status:
            return f"Referral by {self.referred_by.username} for {self.status.title}"
        return f"Referral by {self.referred_by.username}"


class ProfanityWordManager(models.Manager):
    def get_instance(self):
        obj, created = self.get_or_create(id=1)
        return obj

class ProfanityWord(models.Model):
    word_list = models.JSONField(default=list)

    objects = ProfanityWordManager()

    def __str__(self):
        return "Profanity Words"

    def save(self, *args, **kwargs):
        self.word_list = sorted(list(set(self.word_list)), key=lambda x: x.lower())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Profanity Word"
        verbose_name_plural = "Profanity Words"

class Reply(models.Model):
    status = models.ForeignKey(
        'Status',
        related_name='replies',
        on_delete=models.CASCADE
    )
    parent_reply = models.ForeignKey(
        'self',
        related_name='nested_replies',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.status.title}"

class ChatSession(models.Model):
    user = models.ForeignKey(CustomUser, related_name='user_chats', on_delete=models.CASCADE)
    counselor = models.ForeignKey(CustomUser, related_name='counselor_chats', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    last_message_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ChatSession between {self.user.username} and {self.counselor.username}"

    class Meta:
        indexes = [
            models.Index(fields=['user', 'counselor', 'is_active']),
            models.Index(fields=['last_message_at']),
        ]

class CounselorMessage(models.Model):
    chat_session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} at {self.timestamp}"

    class Meta:
        indexes = [
            models.Index(fields=['chat_session', 'timestamp']),
        ]

class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True, null=True)
    is_replied = models.BooleanField(default=False)

    def __str__(self):
        return f"Contact Us from {self.name}"
    
class UserSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_sessions'
    )
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expire_date = models.DateTimeField()
    session_end = models.DateTimeField(null=True, blank=True)  # To mark logout time

    def __str__(self):
        return f"Session for {self.user.username} - {self.session_key}"

# # Signal Receivers
# @receiver(post_save, sender=CustomUser)
# def create_user_notification_settings(sender, instance, created, **kwargs):
#     if created:
#         UserNotificationSettings.objects.create(user=instance)

# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=CustomUser)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()