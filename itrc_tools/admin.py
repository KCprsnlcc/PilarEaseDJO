# itrc_tools/admin.py

from django.contrib import admin
from .models import (
    VerificationRequest,
    EnrollmentMasterlist,
    SystemSetting,
    AuditLog,
    AuditLogEntry,
    Notification_System,
    CustomUser
)

@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('user__username', 'user__student_id', 'user__email')

@admin.register(EnrollmentMasterlist)
class EnrollmentMasterlistAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'academic_year_level')
    search_fields = ('student_id', 'full_name')
    list_filter = ('academic_year_level',)

@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'details', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'details')

@admin.register(AuditLogEntry)
class AuditLogEntryAdmin(admin.ModelAdmin):
    list_display = ('audit_log', 'description', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('audit_log__user__username', 'description')

@admin.register(Notification_System)
class NotificationSystemAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'message', 'is_read', 'timestamp')
    list_filter = ('notification_type', 'is_read', 'timestamp')
    search_fields = ('user__username', 'message')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'student_id', 'full_name', 'is_itrc_staff', 'is_counselor', 'is_active', 'verification_status')
    search_fields = ('username', 'email', 'student_id', 'full_name')
    list_filter = ('is_itrc_staff', 'is_counselor', 'is_active', 'verification_status')
    readonly_fields = ('date_joined', 'last_login')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('profile')  # Optimize queries if you have related profiles

    def profile_avatar(self, obj):
        return obj.profile.avatar.url if obj.profile.avatar else "No Avatar"
    profile_avatar.short_description = 'Avatar'