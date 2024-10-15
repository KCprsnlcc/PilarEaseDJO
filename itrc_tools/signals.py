# itrc_tools/signals.py

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import SessionLog
from django.utils import timezone

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    # Create a new SessionLog entry when a user logs in
    SessionLog.objects.create(user=user, session_start=timezone.now())

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user:
        # Find the latest SessionLog without a session_end
        try:
            session = SessionLog.objects.filter(user=user, session_end__isnull=True).latest('session_start')
            session.session_end = timezone.now()
            session.save()
        except SessionLog.DoesNotExist:
            # No active session found; you might want to handle this case
            pass
