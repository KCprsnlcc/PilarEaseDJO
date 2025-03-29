from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import (
    Appointment, 
    AppointmentNotification, 
    AppointmentStatus
)

@receiver(post_save, sender=Appointment)
def create_appointment_notification(sender, instance, created, **kwargs):
    """Create notifications when appointment is created or status changes"""
    if created:
        # Notify user that appointment request has been submitted
        AppointmentNotification.objects.create(
            user=instance.user,
            appointment=instance,
            message=f"Your appointment request '{instance.title}' with {instance.counselor.full_name} has been submitted and is pending approval."
        )
        
        # Notify counselor about the new appointment request
        AppointmentNotification.objects.create(
            user=instance.counselor,
            appointment=instance,
            message=f"New appointment request from {instance.user.full_name}: '{instance.title}'"
        )
    else:
        # Get previous state from the database
        try:
            previous_state = Appointment.objects.get(pk=instance.pk)
            
            # If status changed, create notifications
            if previous_state.status != instance.status:
                # Notification for user
                user_message = f"Your appointment '{instance.title}' with {instance.counselor.full_name} has been {instance.status}."
                AppointmentNotification.objects.create(
                    user=instance.user,
                    appointment=instance,
                    message=user_message
                )
                
                # Notification for counselor
                counselor_message = f"Appointment '{instance.title}' with {instance.user.full_name} is now {instance.status}."
                AppointmentNotification.objects.create(
                    user=instance.counselor,
                    appointment=instance,
                    message=counselor_message
                )
        except Appointment.DoesNotExist:
            pass

@receiver(pre_save, sender=Appointment)
def auto_complete_appointments(sender, instance, **kwargs):
    """
    Automatically mark appointments as completed once they're past their end time
    """
    if instance.pk:  # Only for existing appointments (not new ones)
        # Check if it's an existing appointment and status is APPROVED
        current_time = timezone.now()
        appointment_end = timezone.make_aware(
            timezone.datetime.combine(instance.date, instance.end_time)
        ) if timezone.is_naive(timezone.datetime.combine(instance.date, instance.end_time)) else timezone.datetime.combine(instance.date, instance.end_time)
        
        # If the appointment is in the past and still in APPROVED status, mark it as COMPLETED
        if (
            instance.status == AppointmentStatus.APPROVED and 
            current_time > appointment_end
        ):
            instance.status = AppointmentStatus.COMPLETED
