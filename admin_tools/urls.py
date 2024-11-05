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
    path('referrals/', views.referral_view, name='manage_referrals'),
    path('referrals/<int:referral_id>/', views.referral_detail_view, name='referral_detail'),

    # Profanity Management
    path('profanities/', views.profanity_list, name='manage_profanities'),
    path('profanities/add/', views.add_profanity, name='add_profanity'),
    path('profanities/delete/', views.delete_profanity, name='delete_profanity'),

    # API Endpoints
    path('api/referrals/', views.referrals_api, name='referrals_api'),
    path('api/referrals/<int:referral_id>/', views.get_referral_details, name='api_get_referral_details'),
    path('profanities/add/', views.add_profanity_api, name='add_profanity_api'),
    path('profanities/delete/', views.delete_profanity_api, name='delete_profanity_api'),
    # Performance Matrix
    path('performance_dashboard/', views.performance_dashboard, name='performance_dashboard'),
    path('get_progress/<int:dataset_id>/', views.get_progress, name='get_progress'),

    # Chat
    path('chat/', views.chat_view, name='chat'),
    path('chat/get_user_questionnaire/<int:user_id>/', views.get_user_questionnaire, name='get_user_questionnaire'),

    # Analysis
    path('analysis/', views.analysis_view, name='analysis'),

    # Settings
    path('settings/', views.settings, name='settings'),

    # Authentication
    path('login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
]
