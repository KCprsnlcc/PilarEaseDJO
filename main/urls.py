from django.urls import path, include
from main import views  # Adjust this import if your views are in a different app
from django.urls import path
from .views import register_view, login_view, logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Your home view
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('submit_status/', views.submit_status, name='submit_status'),
    path('get_all_statuses/', views.get_all_statuses, name='get_all_statuses'), 
    path('status/<int:status_id>/', views.status_detail, name='status_detail'),
    path('add_reply/<int:status_id>/', views.add_reply, name='add_reply'),
    path('submit_reply/<int:status_id>/', views.submit_reply, name='submit_reply'),
    path('delete_status/<int:status_id>/', views.delete_status, name='delete_status'),
    path('get_user_profile/', views.get_user_profile, name='get_user_profile'),
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
    path('password_manager/', views.password_manager_view, name='password_manager'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('logout/', logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)