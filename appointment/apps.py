from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointment'
    verbose_name = 'Appointment Management'

    def ready(self):
        import appointment.signals
