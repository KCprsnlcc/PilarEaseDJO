# admin_tools/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login_view, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('analytics/', views.analytics, name='analytics'),
    path('status/', views.status, name='status'),
    path('replies/', views.replies, name='replies'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.admin_logout, name='admin_logout'),
]
