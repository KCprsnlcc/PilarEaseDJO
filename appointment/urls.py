from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
    # Dashboard
    path('', views.appointment_dashboard, name='dashboard'),
    
    # Calendar Management
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/events/', views.get_calendar_events, name='calendar_events'),
    path('calendar/block/', views.add_blocked_slot, name='add_blocked_slot'),
    path('calendar/block/<int:slot_id>/remove/', views.remove_blocked_slot, name='remove_blocked_slot'),
    path('calendar/schedule/', views.add_available_schedule, name='add_available_schedule'),
    
    # Appointment Requests
    path('requests/', views.appointment_requests, name='appointment_requests'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointment/<int:appointment_id>/update/', views.update_appointment_status, name='update_appointment_status'),
    
    # Appointment History
    path('history/', views.appointment_history, name='appointment_history'),
    
    # Feedback
    path('feedback/', views.feedback_list, name='feedback'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    path('reports/<int:report_id>/download/<str:format>/', views.download_report, name='download_report'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
]
