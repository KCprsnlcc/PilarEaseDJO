from django.core.management.base import BaseCommand
from main.models import CustomUser, UserProfile

class Command(BaseCommand):
    help = 'Create user profiles for users without one'

    def handle(self, *args, **kwargs):
        users_without_profiles = CustomUser.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Profile created for user {user.username}'))
        self.stdout.write(self.style.SUCCESS('All profiles created successfully'))
