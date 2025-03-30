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
    path('calendar/block/<int:blocked_time_id>/edit/', views.edit_blocked_time, name='edit_blocked_time'),
    path('calendar/block/<int:blocked_time_id>/delete/', views.delete_blocked_time, name='delete_blocked_time'),
    path('calendar/schedule/', views.add_available_schedule, name='add_available_schedule'),
    path('calendar/appointment/create/', views.create_appointment, name='create_appointment'),
    
    # API endpoints for time slots
    path('api/available-slots/', views.available_time_slots, name='available_time_slots'),
    path('api/available-dates/', views.available_dates, name='available_dates'),
    path('api/user-appointments/', views.appointment_history, name='api_user_appointments'),
    path('api/cancel-appointment/<int:appointment_id>/', views.update_appointment_status, name='api_cancel_appointment'),
    
    # Appointment Requests
    path('requests/', views.appointment_requests, name='appointment_requests'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointment/<int:appointment_id>/update-status/', views.update_appointment_status, name='update_appointment_status'),
    path('appointment/<int:appointment_id>/edit/', views.edit_appointment, name='edit_appointment'),
    
    # Appointment History
    path('history/', views.appointment_history, name='appointment_history'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/export-csv/', views.export_csv, name='export_csv'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    path('reports/<int:report_id>/download/<str:format>/', views.download_report, name='download_report'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
]
