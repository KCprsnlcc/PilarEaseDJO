from django.urls import path, include
from main import views  # Adjust this import if your views are in a different app
from .views import register_view, login_view, logout_view, contact_us_view, get_status, refer_status, save_questionnaire
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Your home view
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('submit_status/', views.submit_status, name='submit_status'),
    path('check_profanity/', views.check_profanity, name='check_profanity'),
    path('get_all_statuses/', views.get_all_statuses, name='get_all_statuses'), 
    path('get_status/<int:status_id>/', get_status, name='get_status'),
    path('refer_status/<int:status_id>/', views.refer_status, name='refer_status'),
    path('status/<int:status_id>/', views.status_detail, name='status_detail'),
    path('add_reply/<int:status_id>/', views.add_reply, name='add_reply'),
    path('submit_reply/<int:status_id>/', views.submit_reply, name='submit_reply'),
    path('delete_status/<int:status_id>/', views.delete_status, name='delete_status'),
    path('get_user_profile/', views.get_user_profile, name='get_user_profile'),
    path('chat/', views.chat_view, name='chat_view'),
    path('save_chat_session/', views.save_chat_session, name='save_chat_session'),
    path('save_questionnaire/', views.save_questionnaire, name='save_questionnaire'),
    path('send_message/', views.send_chat_message, name='send_chat_message'),
    path('get_messages/', views.get_chat_messages, name='get_chat_messages'),
    path('contact_us/', contact_us_view, name='contact_us'),
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
    path('password_manager/', views.password_manager_view, name='password_manager'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('logout/', logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)