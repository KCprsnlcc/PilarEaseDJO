# admin_tools/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('sentiment-analytics/', views.sentiment_analytics_view, name='sentiment_analytics'),
    path('generate-wordcloud/', views.generate_wordcloud, name='generate_wordcloud'),
    path('replies/', views.replies_view, name='replies'),
    path('delete-reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('status/', views.status_view, name='status'),
    path('approve-feedback/<int:feedback_id>/', views.approve_feedback, name='approve_feedback'),
    path('delete-feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('approve-testimonial/<int:testimonial_id>/', views.approve_testimonial, name='approve_testimonial'),
    path('delete-testimonial/<int:testimonial_id>/', views.delete_testimonial, name='delete_testimonial'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('manage-referral/', views.manage_referral, name='manage_referral'),
    path('chat/', views.chat, name='chat'),
    path('analysis/', views.analysis_view, name='analysis'),
    path('manage-users/', views.manage_users_view, name='manage_users'),
    path('block-user/', views.block_user, name='block_user'),
    path('contact-us-reply/<int:contact_id>/', views.contact_us_reply, name='contact_us_reply'),
    path('delete-contact-us/<int:contact_id>/', views.delete_contact_us, name='delete_contact_us'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('settings/', views.settings, name='settings'),
     path('referral/', views.manage_referral, name='referral'),
    path('referral/<int:referral_id>/', views.get_referral_details, name='get_referral_details'),
    path('manage_profanities/', views.manage_referral, name='manage_profanities'),  # Reuse manage_referral view
    path('referral/<int:referral_id>/', views.get_referral_details, name='get_referral_details'),
    path('add_profanity/', views.add_profanity, name='add_profanity'),
    path('delete_profanity/', views.delete_profanity, name='delete_profanity'),
    # Referral API (optional)
    path('api/referrals/', views.referrals_api, name='referrals_api'),
    path('api/referral/<int:referral_id>/', views.get_referral_details, name='get_referral_details'),
    path('api/profanity/add/', views.add_profanity, name='add_profanity'),
    path('api/profanity/delete/', views.delete_profanity, name='delete_profanity'),
    path('login/', views.admin_login_view, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
]
