# admin_tools/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Statistics
    path('statistics/', views.statistics_view, name='statistics'),
    path('sentiment-analytics/', views.sentiment_analytics_view, name='sentiment_analytics'),
    path('generate-wordcloud/', views.generate_wordcloud, name='generate_wordcloud'),

    # Replies
    path('replies/', views.replies_view, name='replies'),
    path('delete-reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),

    # Status Management
    path('status/', views.status_view, name='status'),

    # Feedback Management
    path('approve-feedback/<int:feedback_id>/', views.approve_feedback, name='approve_feedback'),
    path('delete-feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),

    # Testimonial Management
    path('approve-testimonial/<int:testimonial_id>/', views.approve_testimonial, name='approve_testimonial'),
    path('delete-testimonial/<int:testimonial_id>/', views.delete_testimonial, name='delete_testimonial'),
    path('exclude_testimonial/<int:testimonial_id>/', views.exclude_testimonial, name='exclude_testimonial'),
    path('unexclude_testimonial/<int:testimonial_id>/', views.unexclude_testimonial, name='unexclude_testimonial'),

    # Contact Us Management
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('contact-us-reply/<int:contact_id>/', views.contact_us_reply, name='contact_us_reply'),
    path('delete-contact-us/<int:contact_id>/', views.delete_contact_us, name='delete_contact_us'),

    # Referral Management
    path('referrals/', views.manage_referrals_view, name='manage_referrals'),
       path('referrals/<int:referral_id>/', views.get_referral_details, name='get_referral_details'),

    # Profanity Management
    path('profanities/', views.manage_profanities_view, name='manage_profanities'),
    path('profanities/add/', views.add_profanity, name='add_profanity'),
    path('profanities/delete/<int:profanity_id>/', views.delete_profanity, name='delete_profanity'),

    # API Endpoints
    path('api/referrals/', views.referrals_api, name='referrals_api'),
    path('api/referrals/<int:referral_id>/', views.get_referral_details, name='api_get_referral_details'),
    path('api/profanities/add/', views.add_profanity_api, name='api_add_profanity'),
    path('api/profanities/delete/<int:profanity_id>/', views.delete_profanity_api, name='api_delete_profanity'),

    # User Management
    path('manage-users/', views.manage_users_view, name='manage_users'),
    path('block-user/', views.block_user, name='block_user'),
    path('block-user/<int:user_id>/', views.block_user, name='block_user'),  # Added user_id for blocking specific users
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    # Chat
    path('chat/', views.chat, name='chat'),

    # Analysis
    path('analysis/', views.analysis_view, name='analysis'),

    # Settings
    path('settings/', views.settings, name='settings'),

    # Authentication
    path('login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
]
