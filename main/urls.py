from django.urls import path
from main import views  # Import your views here
from .views import (
    register_view, 
    login_view, 
    logout_view, 
    contact_us_view, 
    get_status, 
    custom_password_reset_view, 
    custom_password_reset_done_view,
    custom_password_reset_confirm_view,
    custom_password_reset_complete_view, 
    verify_email, check_email_verification, 
    send_verification_email, request_email_change, 
    verify_email_change, request_email_verification
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Your home view
    path('register/', register_view, name='register'),
    path('request_email_change/', request_email_change, name='request_email_change'),
    path('verify_email_change/<uidb64>/<token>/<new_email>/', verify_email_change, name='verify_email_change'),
    path('verify_email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('check_email_verification/', check_email_verification, name='check_email_verification'),
    path('send_verification_email/', send_verification_email, name='send_verification_email'),
    path('request_email_verification/', request_email_verification, name='request_email_verification'),
    path('login/', login_view, name='login'),
    path('password-reset/', custom_password_reset_view, name='password_reset'),  # Custom password reset view
    path('password-reset/done/', custom_password_reset_done_view, name='password_reset_done'),  # Custom password reset done view
    path('reset/<uidb64>/<token>/', custom_password_reset_confirm_view, name='password_reset_confirm'),  # Custom password reset confirm view
    path('reset/done/', custom_password_reset_complete_view, name='password_reset_complete'),  # Custom password reset complete view
    path('submit_status/', views.submit_status, name='submit_status'), 
    path('fetch_notifications/', views.fetch_notifications, name='fetch_notifications'),
    path('notifications/fetch/', views.fetch_notifications, name='fetch_notifications'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/mark_button_clicked/', views.mark_notification_button_clicked, name='mark_notification_button_clicked'),
    path('notifications/check_status/', views.check_notification_status, name='check_notification_status'),
    path('check_profanity/', views.check_profanity, name='check_profanity'),
    path('get_all_statuses/', views.get_all_statuses, name='get_all_statuses'), 
    path('get_status/<int:status_id>/', get_status, name='get_status'),
    path('refer_status/<int:status_id>/', views.refer_status, name='refer_status'),
    path('status/<int:status_id>/', views.status_detail, name='status_detail'),
    path('add_reply/<int:status_id>/', views.add_reply, name='add_reply'),
    path('submit_reply/<int:status_id>/', views.submit_reply, name='submit_reply'),
    path('delete_status/<int:status_id>/', views.delete_status, name='delete_status'),
    path('get_user_profile/', views.get_user_profile, name='get_user_profile'),
    path('save_chat_session/', views.save_chat_session, name='save_chat_session'),
    path('load_chat_session/', views.load_chat_session, name='load_chat_session'),
    path('save_questionnaire/', views.save_questionnaire, name='save_questionnaire'),
    path('contact_us/', contact_us_view, name='contact_us'),
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
    path('password_manager/', views.password_manager_view, name='password_manager'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('logout/', logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)