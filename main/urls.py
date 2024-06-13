from django.urls import path, include
from main import views  # Adjust this import if your views are in a different app
from django.urls import path
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('', views.home, name='home'),  # Your home view
    path('', register_view, name='register'),
    path('', login_view, name='login'),
    path('', logout_view, name='logout'),
]


