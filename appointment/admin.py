from django.contrib import admin
from .models import (
    AppointmentSchedule,
    Appointment,
    AppointmentFeedback,
    BlockedTimeSlot,
    AppointmentNotification,
    AppointmentReport
)

@admin.register(AppointmentSchedule)
class AppointmentScheduleAdmin(admin.ModelAdmin):
    list_display = ('counselor', 'date', 'start_time', 'end_time', 'is_available')
    list_filter = ('is_available', 'date', 'counselor')
    search_fields = ('counselor__username', 'counselor__full_name')
    date_hierarchy = 'date'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'counselor', 'title', 'date', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'date', 'counselor')
    search_fields = ('title', 'description', 'user__username', 'counselor__username')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AppointmentFeedback)
class AppointmentFeedbackAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('appointment__title', 'comments', 'suggestions')
    readonly_fields = ('created_at',)

@admin.register(BlockedTimeSlot)
class BlockedTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('counselor', 'date', 'start_time', 'end_time', 'reason')
    list_filter = ('date', 'counselor')
    search_fields = ('reason', 'counselor__username')
    date_hierarchy = 'date'

@admin.register(AppointmentNotification)
class AppointmentNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'appointment', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    readonly_fields = ('created_at',)

@admin.register(AppointmentReport)
class AppointmentReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'start_date', 'end_date', 'generated_by', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('title', 'generated_by__username')
    readonly_fields = ('created_at', 'data')
