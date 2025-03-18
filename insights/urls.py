from django.urls import path
from .views import insights_dashboard, user_analysis

urlpatterns = [
    path('dashboard/', insights_dashboard, name='insights_dashboard'),
    path('user/<int:user_id>/', user_analysis, name='user_analysis'),
]
