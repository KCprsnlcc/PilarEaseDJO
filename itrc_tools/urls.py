# itrc_tools/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ItrcLoginView.as_view(), name='itrc_login'),  # Root path for ITRC login
    path('dashboard/', views.itrc_dashboard, name='itrc_dashboard'),
    path('verify-user/<int:user_id>/', views.verify_user, name='verify_user'),
    path('upload-masterlist/', views.upload_masterlist, name='upload_masterlist'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('system-settings/', views.system_settings, name='system_settings'),
    path('generate-reports/', views.generate_reports, name='generate_reports'),
]
