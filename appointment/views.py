from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.urls import reverse
from datetime import datetime, timedelta
import json
import csv
import io
import xlsxwriter
from .models import (
    AppointmentSchedule,
    Appointment,
    AppointmentFeedback,
    BlockedTimeSlot,
    AppointmentNotification,
    AppointmentReport,
    AppointmentStatus
)
from .forms import (
    AppointmentScheduleForm,
    AppointmentForm,
    UpdateAppointmentStatusForm,
    AppointmentFeedbackForm,
    BlockedTimeSlotForm,
    AppointmentReportForm,
    DateRangeFilterForm
)

# Helper functions
def is_counselor_or_staff(user):
    return user.is_authenticated and (user.is_counselor or user.is_itrc_staff)

# Dashboard view
@login_required
@user_passes_test(is_counselor_or_staff)
def appointment_dashboard(request):
    """Main dashboard for the appointment management system"""
    today = timezone.now().date()
    
    # Get counts for various appointment statuses
    pending_count = Appointment.objects.filter(status=AppointmentStatus.PENDING).count()
    upcoming_count = Appointment.objects.filter(
        status=AppointmentStatus.APPROVED,
        date__gte=today
    ).count()
    completed_count = Appointment.objects.filter(status=AppointmentStatus.COMPLETED).count()
    cancelled_count = Appointment.objects.filter(status=AppointmentStatus.CANCELLED).count()
    
    # Get today's appointments
    todays_appointments = Appointment.objects.filter(
        date=today
    ).order_by('start_time')
    
    # Get recent notifications
    recent_notifications = AppointmentNotification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    # Upcoming appointments (next 7 days)
    next_week = today + timedelta(days=7)
    upcoming_appointments = Appointment.objects.filter(
        date__gte=today,
        date__lte=next_week,
        status=AppointmentStatus.APPROVED
    ).order_by('date', 'start_time')[:5]
    
    context = {
        'pending_count': pending_count,
        'upcoming_count': upcoming_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'todays_appointments': todays_appointments,
        'recent_notifications': recent_notifications,
        'upcoming_appointments': upcoming_appointments,
    }
    
    return render(request, 'appointment/dashboard.html', context)

# Calendar views
@login_required
@user_passes_test(is_counselor_or_staff)
def calendar_view(request):
    """Calendar view showing all scheduled appointments"""
    today = timezone.now().date()
    blocked_slots = BlockedTimeSlot.objects.all()
    
    # Get events for calendar (appointments and blocked slots)
    appointments = Appointment.objects.filter(
        Q(counselor=request.user) | Q(user=request.user)
    ).exclude(status=AppointmentStatus.CANCELLED)
    
    # Form for adding new blocked time slots
    form = BlockedTimeSlotForm(initial={'counselor': request.user})
    
    # If the user is a counselor, get their available schedules
    if request.user.is_counselor:
        available_schedules = AppointmentSchedule.objects.filter(
            counselor=request.user,
            is_available=True
        )
    else:
        available_schedules = AppointmentSchedule.objects.filter(
            is_available=True
        )
    
    context = {
        'appointments': appointments,
        'blocked_slots': blocked_slots,
        'available_schedules': available_schedules,
        'form': form,
        'today': today,
    }
    
    return render(request, 'appointment/calendar.html', context)

@login_required
@user_passes_test(is_counselor_or_staff)
def get_calendar_events(request):
    """API endpoint to get events for the calendar (AJAX)"""
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    if start and end:
        start_date = datetime.fromisoformat(start.split('T')[0])
        end_date = datetime.fromisoformat(end.split('T')[0])
        
        # Get appointments
        appointments = Appointment.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).exclude(status=AppointmentStatus.CANCELLED)
        
        # Get blocked slots
        blocked_slots = BlockedTimeSlot.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        )
        
        # Get available schedules
        available_schedules = AppointmentSchedule.objects.filter(
            date__gte=start_date,
            date__lte=end_date,
            is_available=True
        )
        
        # Format events for calendar
        events = []
        
        # Add appointments
        for appointment in appointments:
            event = {
                'id': f'appointment_{appointment.id}',
                'title': appointment.title,
                'start': f"{appointment.date.isoformat()}T{appointment.start_time.isoformat()}",
                'end': f"{appointment.date.isoformat()}T{appointment.end_time.isoformat()}",
                'backgroundColor': get_status_color(appointment.status),
                'borderColor': get_status_color(appointment.status),
                'extendedProps': {
                    'status': appointment.status,
                    'type': 'appointment',
                    'description': appointment.description,
                    'user': appointment.user.full_name,
                    'counselor': appointment.counselor.full_name,
                }
            }
            events.append(event)
        
        # Add blocked slots
        for slot in blocked_slots:
            event = {
                'id': f'blocked_{slot.id}',
                'title': 'Blocked: ' + (slot.reason or 'No reason provided'),
                'start': f"{slot.date.isoformat()}T{slot.start_time.isoformat()}",
                'end': f"{slot.date.isoformat()}T{slot.end_time.isoformat()}",
                'backgroundColor': '#dc3545',
                'borderColor': '#dc3545',
                'extendedProps': {
                    'type': 'blocked',
                    'counselor': slot.counselor.full_name,
                }
            }
            events.append(event)
            
        # Add available schedules
        for schedule in available_schedules:
            event = {
                'id': f'available_{schedule.id}',
                'title': 'Available',
                'start': f"{schedule.date.isoformat()}T{schedule.start_time.isoformat()}",
                'end': f"{schedule.date.isoformat()}T{schedule.end_time.isoformat()}",
                'backgroundColor': '#28a745',
                'borderColor': '#28a745',
                'extendedProps': {
                    'type': 'available',
                    'counselor': schedule.counselor.full_name,
                }
            }
            events.append(event)
        
        return JsonResponse(events, safe=False)
    
    return JsonResponse([], safe=False)

def get_status_color(status):
    """Get color for appointment status"""
    colors = {
        AppointmentStatus.PENDING: '#ffc107',  # Yellow
        AppointmentStatus.APPROVED: '#28a745',  # Green
        AppointmentStatus.CANCELLED: '#dc3545',  # Red
        AppointmentStatus.COMPLETED: '#007bff',  # Blue
        AppointmentStatus.RESCHEDULED: '#6c757d',  # Gray
        AppointmentStatus.NO_SHOW: '#343a40',  # Dark Gray
    }
    return colors.get(status, '#6c757d')

@login_required
@user_passes_test(is_counselor_or_staff)
def add_blocked_slot(request):
    """Add a new blocked time slot"""
    if request.method == 'POST':
        form = BlockedTimeSlotForm(request.POST)
        if form.is_valid():
            blocked_slot = form.save(commit=False)
            if not hasattr(blocked_slot, 'counselor') or not blocked_slot.counselor:
                blocked_slot.counselor = request.user
            blocked_slot.save()
            messages.success(request, 'Time slot blocked successfully.')
            return redirect('appointment:calendar')
        else:
            messages.error(request, 'Error blocking time slot. Please check the form.')
    
    return redirect('appointment:calendar')

@login_required
@user_passes_test(is_counselor_or_staff)
def remove_blocked_slot(request, slot_id):
    """Remove a blocked time slot"""
    slot = get_object_or_404(BlockedTimeSlot, id=slot_id)
    slot.delete()
    messages.success(request, 'Blocked time slot removed successfully.')
    return redirect('appointment:calendar')

@login_required
@user_passes_test(is_counselor_or_staff)
def add_available_schedule(request):
    """Add a new available schedule"""
    if request.method == 'POST':
        form = AppointmentScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            if not hasattr(schedule, 'counselor') or not schedule.counselor:
                schedule.counselor = request.user
            schedule.save()
            messages.success(request, 'Available schedule added successfully.')
            return redirect('appointment:calendar')
        else:
            messages.error(request, 'Error adding schedule. Please check the form.')
    
    return redirect('appointment:calendar')

# Appointment request views
@login_required
@user_passes_test(is_counselor_or_staff)
def appointment_requests(request):
    """View to manage appointment requests"""
    # Get appointment requests
    pending_appointments = Appointment.objects.filter(
        status=AppointmentStatus.PENDING
    ).order_by('date', 'start_time')
    
    # Paginate results
    paginator = Paginator(pending_appointments, 10)
    page_number = request.GET.get('page', 1)
    pending_appointments = paginator.get_page(page_number)
    
    context = {
        'pending_appointments': pending_appointments,
    }
    
    return render(request, 'appointment/requests.html', context)

@login_required
@user_passes_test(is_counselor_or_staff)
def appointment_detail(request, appointment_id):
    """View details of a specific appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Form for updating appointment status
    form = UpdateAppointmentStatusForm(instance=appointment)
    
    if request.method == 'POST':
        form = UpdateAppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            send_notification = form.cleaned_data.get('send_notification', False)
            
            if send_notification:
                # Create notification for the user
                AppointmentNotification.objects.create(
                    user=appointment.user,
                    appointment=appointment,
                    message=f"Your appointment '{appointment.title}' has been updated to {appointment.get_status_display()}."
                )
            
            messages.success(request, 'Appointment updated successfully.')
            return redirect('appointment:appointment_detail', appointment_id=appointment.id)
    
    context = {
        'appointment': appointment,
        'form': form,
    }
    
    return render(request, 'appointment/appointment_detail.html', context)

@login_required
@user_passes_test(is_counselor_or_staff)
def update_appointment_status(request, appointment_id):
    """Update the status of an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = UpdateAppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment status updated successfully.')
            
            # Redirect back to the appropriate page
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('appointment:appointment_requests')
    
    return redirect('appointment:appointment_detail', appointment_id=appointment.id)

# Appointment history views
@login_required
@user_passes_test(is_counselor_or_staff)
def appointment_history(request):
    """View appointment history"""
    # Filter form
    filter_form = DateRangeFilterForm(request.GET)
    
    # Base queryset
    appointments = Appointment.objects.all().order_by('-date', '-start_time')
    
    # Apply filters if form is valid
    if filter_form.is_valid():
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')
        
        if start_date:
            appointments = appointments.filter(date__gte=start_date)
        if end_date:
            appointments = appointments.filter(date__lte=end_date)
    
    # Status filter
    status = request.GET.get('status')
    if status:
        appointments = appointments.filter(status=status)
    
    # Filter by user/counselor if specified
    user_id = request.GET.get('user')
    if user_id:
        appointments = appointments.filter(user_id=user_id)
    
    counselor_id = request.GET.get('counselor')
    if counselor_id:
        appointments = appointments.filter(counselor_id=counselor_id)
    
    # Paginate results
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page', 1)
    appointments = paginator.get_page(page_number)
    
    context = {
        'appointments': appointments,
        'filter_form': filter_form,
        'statuses': AppointmentStatus.choices,
    }
    
    return render(request, 'appointment/history.html', context)

# Feedback views
@login_required
@user_passes_test(is_counselor_or_staff)
def feedback_list(request):
    """View feedback from appointments"""
    feedback = AppointmentFeedback.objects.all().order_by('-created_at')
    
    # Filter by rating if specified
    rating = request.GET.get('rating')
    if rating and rating.isdigit():
        feedback = feedback.filter(rating=int(rating))
    
    # Paginate results
    paginator = Paginator(feedback, 10)
    page_number = request.GET.get('page', 1)
    feedback = paginator.get_page(page_number)
    
    # Calculate average rating
    avg_rating = AppointmentFeedback.objects.aggregate(
        avg_rating=models.Avg('rating')
    )['avg_rating'] or 0
    
    context = {
        'feedback': feedback,
        'avg_rating': round(avg_rating, 1),
    }
    
    return render(request, 'appointment/feedback.html', context)

# Reports views
@login_required
@user_passes_test(is_counselor_or_staff)
def reports(request):
    """Generate and view appointment reports"""
    # Reports form
    form = AppointmentReportForm()
    
    if request.method == 'POST':
        form = AppointmentReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.generated_by = request.user
            
            # Get data for the report
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Get appointments in the date range
            appointments = Appointment.objects.filter(
                date__gte=start_date,
                date__lte=end_date
            )
            
            # Generate report data
            report_data = generate_report_data(appointments)
            report.data = report_data
            report.save()
            
            messages.success(request, 'Report generated successfully.')
            return redirect('appointment:report_detail', report_id=report.id)
    
    # Get existing reports
    reports = AppointmentReport.objects.all().order_by('-created_at')
    
    # Paginate results
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page', 1)
    reports = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'reports': reports,
    }
    
    return render(request, 'appointment/reports.html', context)

def generate_report_data(appointments):
    """Generate data for appointment report"""
    # Count appointments by status
    status_counts = {
        status: appointments.filter(status=status).count()
        for status, _ in AppointmentStatus.choices
    }
    
    # Count appointments by counselor
    counselor_counts = {}
    for appointment in appointments:
        counselor_name = appointment.counselor.full_name
        if counselor_name in counselor_counts:
            counselor_counts[counselor_name] += 1
        else:
            counselor_counts[counselor_name] = 1
    
    # Group appointments by date
    date_counts = {}
    for appointment in appointments:
        date_str = appointment.date.isoformat()
        if date_str in date_counts:
            date_counts[date_str] += 1
        else:
            date_counts[date_str] = 1
    
    # Return compiled data
    return {
        'total_appointments': appointments.count(),
        'status_counts': status_counts,
        'counselor_counts': counselor_counts,
        'date_counts': date_counts,
    }

@login_required
@user_passes_test(is_counselor_or_staff)
def report_detail(request, report_id):
    """View details of a specific report"""
    report = get_object_or_404(AppointmentReport, id=report_id)
    
    context = {
        'report': report,
    }
    
    return render(request, 'appointment/report_detail.html', context)

@login_required
@user_passes_test(is_counselor_or_staff)
def download_report(request, report_id, format='csv'):
    """Download report in various formats (CSV, Excel)"""
    report = get_object_or_404(AppointmentReport, id=report_id)
    
    # Get appointments for the report period
    appointments = Appointment.objects.filter(
        date__gte=report.start_date,
        date__lte=report.end_date
    ).order_by('date', 'start_time')
    
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{report.title}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Start Time', 'End Time', 'Title', 'User', 'Counselor', 
            'Status', 'Created At'
        ])
        
        for appointment in appointments:
            writer.writerow([
                appointment.date,
                appointment.start_time,
                appointment.end_time,
                appointment.title,
                appointment.user.full_name,
                appointment.counselor.full_name,
                appointment.get_status_display(),
                appointment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    
    elif format == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Add header
        headers = [
            'Date', 'Start Time', 'End Time', 'Title', 'User', 'Counselor', 
            'Status', 'Created At'
        ]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)
        
        # Add data
        for row_num, appointment in enumerate(appointments, 1):
            worksheet.write(row_num, 0, appointment.date.isoformat())
            worksheet.write(row_num, 1, appointment.start_time.isoformat())
            worksheet.write(row_num, 2, appointment.end_time.isoformat())
            worksheet.write(row_num, 3, appointment.title)
            worksheet.write(row_num, 4, appointment.user.full_name)
            worksheet.write(row_num, 5, appointment.counselor.full_name)
            worksheet.write(row_num, 6, appointment.get_status_display())
            worksheet.write(row_num, 7, appointment.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        
        # Add summary worksheet
        summary = workbook.add_worksheet('Summary')
        summary.write(0, 0, 'Report Summary')
        summary.write(1, 0, 'Title:')
        summary.write(1, 1, report.title)
        summary.write(2, 0, 'Period:')
        summary.write(2, 1, f"{report.start_date} to {report.end_date}")
        summary.write(3, 0, 'Total Appointments:')
        summary.write(3, 1, appointments.count())
        
        # Status summary
        summary.write(5, 0, 'Status')
        summary.write(5, 1, 'Count')
        row = 6
        for status, _ in AppointmentStatus.choices:
            count = appointments.filter(status=status).count()
            summary.write(row, 0, dict(AppointmentStatus.choices)[status])
            summary.write(row, 1, count)
            row += 1
        
        workbook.close()
        
        output.seek(0)
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{report.title}.xlsx"'
        
        return response
    
    # Default: redirect back to report detail
    return redirect('appointment:report_detail', report_id=report.id)

# Notification views
@login_required
@user_passes_test(is_counselor_or_staff)
def notifications(request):
    """View all notifications"""
    notifications = AppointmentNotification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    # Mark all as read if requested
    if request.GET.get('mark_all_read'):
        notifications.update(is_read=True)
        return redirect('appointment:notifications')
    
    # Paginate results
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page', 1)
    notifications = paginator.get_page(page_number)
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'appointment/notifications.html', context)

@login_required
@user_passes_test(is_counselor_or_staff)
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(
        AppointmentNotification, 
        id=notification_id,
        user=request.user
    )
    notification.is_read = True
    notification.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'appointment:notifications'))
