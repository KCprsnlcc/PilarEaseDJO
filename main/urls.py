from django.contrib import admin
from django.urls import path, include
from main import views  # Adjust this import if your views are in a different app

urlpatterns = [
    path('', views.home, name='home'),  # Your home view
]
