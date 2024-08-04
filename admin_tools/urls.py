from django.urls import path
from admin_tools import views

urlpatterns = [
    path('login/', views.admin_login_view, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('statistics/', views.statistics, name='statistics'),
    path('analysis/', views.analysis, name='analysis'),
    path('reports/', views.reports, name='reports'),
    path('status/', views.status, name='status'),
    path('replies/', views.replies, name='replies'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.admin_logout, name='admin_logout'),
]
