from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Root path for ITRC login (Login view will be accessible by default at '/itrc/')
    path('login/', views.ItrcLoginView.as_view(), name='itrc_login'),


    # Dashboard and other ITRC tools accessible only after login
    path('dashboard/', views.itrc_dashboard, name='itrc_dashboard'),
    path('verify-user/<int:user_id>/', views.verify_user, name='verify_user'),
    path('upload-masterlist/', views.upload_masterlist, name='upload_masterlist'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('manage_users/bulk_action/', views.manage_users_bulk_action, name='manage_users_bulk_action'),
    path('audit_logs/', views.audit_logs_view, name='audit_logs'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('system-settings/', views.system_settings, name='system_settings'),
    path('generate-reports/', views.generate_reports, name='generate_reports'),
    path('audit-logs/', views.audit_logs_view, name='audit_logs'),

    # Add a path for logging out
    path('logout/', LogoutView.as_view(next_page='/itrc/'), name='itrc_logout'),
]
