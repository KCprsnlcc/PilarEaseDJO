from django.urls import path, include
from main import views  # Adjust this import if your views are in a different app
from django.urls import path
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('', views.home, name='home'),  # Your home view
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
<<<<<<< HEAD
    path('get_user_profile/', views.get_user_profile, name='get_user_profile'),
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
=======
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
    path('logout/', logout_view, name='logout'),
]


