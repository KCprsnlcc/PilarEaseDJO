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

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    

User = get_user_model()

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
    
class Reply(models.Model):
    status = models.ForeignKey(Status, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
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
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
