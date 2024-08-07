from django.urls import path
from admin_tools import views

urlpatterns = [
    path('dashboard/', views.contact_us_view, name='admin_dashboard'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('analysis/', views.analysis_view, name='analysis'),
    path('reports/', views.reports, name='reports'),
    path('status/', views.status_view, name='status'),
    path('replies/', views.replies_view, name='replies'),
    path('delete_reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('manage_users/', views.manage_users_view, name='manage_users'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
]