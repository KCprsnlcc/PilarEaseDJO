# admin_tools/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Feedback Management URLs
    path('dashboard/approve_feedback/<int:feedback_id>/', views.approve_feedback, name='approve_feedback'),
    path('dashboard/delete_feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    
    # Testimonial Management URLs
    path('dashboard/approve_testimonial/<int:testimonial_id>/', views.approve_testimonial, name='approve_testimonial'),
    path('dashboard/delete_testimonial/<int:testimonial_id>/', views.delete_testimonial, name='delete_testimonial'),
    
    # Replies Management URLs
    path('replies/', views.replies_view, name='replies'),
    path('replies/delete/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    
    # Status Management URLs
    path('status/', views.status_view, name='status'),
    
    # Statistics URL
    path('statistics/', views.statistics_view, name='statistics'),
    
    # Analysis URL
    path('analysis/', views.analysis_view, name='analysis'),
    
    # Reports URL
    path('reports/', views.reports, name='reports'),
    
    # Manage Users URLs
    path('manage_users/', views.manage_users_view, name='manage_users'),
    path('manage_users/block/', views.block_user, name='block_user'),
    path('manage_users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # Contact Us URLs
    path('contact_us/', views.contact_us_view, name='contact_us'),
    path('contact_us/reply/<int:contact_id>/', views.contact_us_reply, name='contact_us_reply'),
    path('contact_us/delete/<int:contact_id>/', views.delete_contact_us, name='delete_contact_us'),
    
    # Manage Referral URL
    path('manage_referral/', views.manage_referral, name='manage_referral'),
    
    # Chat URL
    path('chat/', views.chat, name='chat'),
    
    # Settings URL
    path('settings/', views.settings, name='settings'),
]
