from django.urls import path
from .views import insights_dashboard, user_analysis, status_details_api, generate_user_report

urlpatterns = [
    path('dashboard/', insights_dashboard, name='insights_dashboard'),
    path('user/<int:user_id>/', user_analysis, name='user_analysis'),
    path('status/<int:status_id>/details/', status_details_api, name='status_details_api'),
    path('user/<int:user_id>/report/', generate_user_report, name='generate_user_report'),
]
