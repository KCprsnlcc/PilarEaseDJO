# main/urls.py
from django.urls import path
from .views import landing

urlpatterns = [
    path('', landing, name='landing'),
    # other URL patterns
]
