# itrc_tools/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.ItrcLoginView.as_view(), name='itrc_login'),
    path('logout/', views.ItrcLogoutView.as_view(), name='itrc_logout'),

    # Dashboard and Management URLs
    path('dashboard/', views.itrc_dashboard, name='itrc_dashboard'),
    path('verify-user/<int:user_id>/', views.verify_user, name='verify_user'),
    path('upload-masterlist/', views.upload_masterlist, name='upload_masterlist'),
    path('add-student-to-masterlist/', views.add_student_to_masterlist, name='add_student_to_masterlist'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-users/bulk-action/', views.manage_users_bulk_action, name='manage_users_bulk_action'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('system-settings/', views.system_settings, name='system_settings'),
    path('generate-reports/', views.generate_reports, name='generate_reports'),
    path('audit-logs/', views.audit_logs_view, name='audit_logs'),
    
    # Notifications URLs
    path('fetch-notifications/', views.fetch_notifications, name='fetch_notifications'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/mark-all-as-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),

    # Contact Support
    path('contact-support/', views.contact_support, name='contact_support'),

    # New User Management URLs
    path('add-user/', views.add_user, name='add_user'),
    path('edit-user/<int:user_id>/', views.edit_user_view, name='edit_user'), # Optional: Implement this view
    path('change-role/<int:user_id>/', views.change_role, name='change_role'),  # Optional: Implement this view
    path('check-unique/', views.check_unique, name='check_unique'),
     path('generate-pdf-report/', views.generate_pdf_report, name='generate_pdf_report'),
    
    # Bulk Verification Actions
    path('auto-accept-all/', views.auto_accept_all, name='auto_accept_all'),
    path('auto-reject-all/', views.auto_reject_all, name='auto_reject_all'),

    # AJAX Endpoints for Toggling Settings
    path('toggle-auto-accept/', views.toggle_auto_accept, name='toggle_auto_accept'),
    path('toggle-auto-reject/', views.toggle_auto_reject, name='toggle_auto_reject'),

    # AJAX Endpoints for Manual Review
    path('manual-accept-user/<int:user_id>/', views.manual_accept_user, name='manual_accept_user'),
    path('manual-reject-user/<int:user_id>/', views.manual_reject_user, name='manual_reject_user'),
    path('fetch-pending-requests/', views.fetch_pending_requests, name='fetch_pending_requests'),
]
    # ... other URL patterns ...

