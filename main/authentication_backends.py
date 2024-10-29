# your_app/authentication_backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomBackend(ModelBackend):
    def user_can_authenticate(self, user):
        # Allow authentication regardless of is_active status
        return True
