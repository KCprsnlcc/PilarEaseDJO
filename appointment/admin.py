from django.contrib import admin
from .models import (
    AppointmentSchedule,
    Appointment,
    BlockedTimeSlot,
    AppointmentNotification,
    AppointmentReport
)

@admin.register(AppointmentSchedule)
class AppointmentScheduleAdmin(admin.ModelAdmin):
    list_display = ('counselor', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
    search_fields = ('counselor__full_name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'counselor', 'date', 'start_time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('title', 'description', 'user__full_name', 'counselor__full_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(BlockedTimeSlot)
class BlockedTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('counselor', 'date', 'start_time', 'end_time', 'reason')
    list_filter = ('date', 'counselor')
    search_fields = ('counselor__full_name', 'reason')
    readonly_fields = ('created_at',)

@admin.register(AppointmentNotification)
class AppointmentNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'appointment', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__full_name', 'appointment__title', 'message')
    readonly_fields = ('created_at',)

@admin.register(AppointmentReport)
class AppointmentReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'generated_by', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('title', 'generated_by__full_name')
    readonly_fields = ('created_at',)
