from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Q, Count, Avg
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
from django.contrib.auth import get_user_model
import random

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
    total_appointments = Appointment.objects.count()
    
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
    upcoming_appointments_list = Appointment.objects.filter(
        date__gte=today,
        date__lte=next_week,
        status=AppointmentStatus.APPROVED
    ).order_by('date', 'start_time')[:5]
    
    # Get all recent appointments for the dashboard table
    recent_appointments = Appointment.objects.all().order_by('-created_at')[:10]
    
    # Get blocked time slots
    blocked_slots = BlockedTimeSlot.objects.filter(
        date__gte=today
    ).order_by('date', 'start_time')[:5]
    
    # Count available slots
    available_slots = AppointmentSchedule.objects.filter(
        date__gte=today,
        is_available=True
    ).count()
    
    # Prepare status counts for chart
    status_counts = {
        'pending': pending_count,
        'approved': upcoming_count,
        'completed': completed_count,
        'cancelled': cancelled_count
    }
    
    # Prepare trend data for chart (last 6 months)
    months = []
    trend_data = []
    
    for i in range(5, -1, -1):
        month_date = today - timedelta(days=30 * i)
        month_name = month_date.strftime('%b')
        months.append(month_name)
        
        month_start = month_date.replace(day=1)
        if i > 0:
            next_month = month_date.replace(day=28) + timedelta(days=4)
            month_end = next_month.replace(day=1) - timedelta(days=1)
        else:
            month_end = today
        
        count = Appointment.objects.filter(
            date__gte=month_start,
            date__lte=month_end
        ).count()
        trend_data.append(count)
    
    context = {
        'pending_count': pending_count,
        'upcoming_count': upcoming_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'total_appointments': total_appointments,
        'todays_appointments': todays_appointments,
        'recent_notifications': recent_notifications,
        'upcoming_appointments': upcoming_appointments_list,
        'recent_appointments': recent_appointments,
        'blocked_slots': blocked_slots,
        'available_slots': available_slots,
        'status_counts': status_counts,
        'trend_labels': months,
        'trend_data': trend_data,
        'pending_appointments': pending_count  # Alias for dashboard summary card
    }
    
    return render(request, 'appointment/dashboard.html', context)

# Calendar views
@login_required
@user_passes_test(is_counselor_or_staff)
def calendar_view(request):
    """View for calendar page"""
    # Get current date
    today = timezone.now().date()
    
    # Get appointments
    appointments = Appointment.objects.all()
    
    # Get blocked time slots
    blocked_slots = BlockedTimeSlot.objects.all()
    
    # Get available schedules
    available_schedules = AppointmentSchedule.objects.all()
    
    # Create appointment form
    form = AppointmentForm(initial={'counselor': request.user})
    
    # Get users for select field
    User = get_user_model()
    users = User.objects.filter(is_counselor=False).order_by('full_name')
    
    context = {
        'appointments': appointments,
        'blocked_slots': blocked_slots,
        'available_schedules': available_schedules,
        'form': form,
        'today': today,
        'users': users,
    }
    
    return render(request, 'appointment/calendar.html', context)

@login_required
@user_passes_test(is_counselor_or_staff)
def get_calendar_events(request):
    """Get calendar events in JSON format"""
        # Get appointments
    appointments = Appointment.objects.all()
    
    # Get blocked time slots
    blocked_slots = BlockedTimeSlot.objects.all()
    
    # Prepare events list
    events = []
        
    # Add appointments to events
    for appointment in appointments:
            event = {
            'id': appointment.id,
            'title': f"{appointment.title} ({appointment.user.full_name})",
                'start': f"{appointment.date.isoformat()}T{appointment.start_time.isoformat()}",
                'end': f"{appointment.date.isoformat()}T{appointment.end_time.isoformat()}",
            'status': appointment.status.lower(),
            'type': 'appointment'
            }
            events.append(event)
        
    # Add blocked time slots to events
    for slot in blocked_slots:
            event = {
            'id': slot.id,
            'title': f"Blocked: {slot.reason}",
                'start': f"{slot.date.isoformat()}T{slot.start_time.isoformat()}",
                'end': f"{slot.date.isoformat()}T{slot.end_time.isoformat()}",
            'status': 'blocked',
            'type': 'blocked'
            }
            events.append(event)
        
    return JsonResponse(events, safe=False)

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
    """View and manage appointment requests"""
    # Filter by status if specified
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    search = request.GET.get('search')
    
    # Start with all appointments for this counselor
    pending_requests_query = Appointment.objects.filter(
        counselor=request.user,
        status=AppointmentStatus.PENDING
    )
    
    all_requests_query = Appointment.objects.filter(
        counselor=request.user
    )
    
    # Apply filters
    if status:
        all_requests_query = all_requests_query.filter(status=status)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            pending_requests_query = pending_requests_query.filter(date__gte=date_from_obj)
            all_requests_query = all_requests_query.filter(date__gte=date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            pending_requests_query = pending_requests_query.filter(date__lte=date_to_obj)
            all_requests_query = all_requests_query.filter(date__lte=date_to_obj)
        except ValueError:
            pass
    
    if search:
        pending_requests_query = pending_requests_query.filter(
            Q(title__icontains=search) | 
            Q(user__full_name__icontains=search)
        )
        all_requests_query = all_requests_query.filter(
            Q(title__icontains=search) | 
            Q(user__full_name__icontains=search)
        )
    
    # Order the results
    pending_requests_query = pending_requests_query.order_by('date', 'start_time')
    all_requests_query = all_requests_query.order_by('-created_at')
    
    # Paginate results
    pending_paginator = Paginator(pending_requests_query, 10)
    all_paginator = Paginator(all_requests_query, 10)
    
    page_number = request.GET.get('page', 1)
    all_page_number = request.GET.get('all_page', 1)
    
    pending_requests = pending_paginator.get_page(page_number)
    all_requests = all_paginator.get_page(all_page_number)
    
    # Get stats for display
    stats = {
        'pending_count': Appointment.objects.filter(counselor=request.user, status=AppointmentStatus.PENDING).count(),
        'approved_count': Appointment.objects.filter(counselor=request.user, status=AppointmentStatus.APPROVED).count(),
        'rejected_count': Appointment.objects.filter(counselor=request.user, status=AppointmentStatus.CANCELLED).count(),
        'total_count': Appointment.objects.filter(counselor=request.user).count()
    }
    
    context = {
        'pending_requests': pending_requests,
        'all_requests': all_requests,
        'stats': stats,
        'selected_status': status
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
    today = timezone.now().date()
    
    # Filter by parameters
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    search = request.GET.get('search')
    
    # Get upcoming appointments (today or future date, approved status)
    upcoming_query = Appointment.objects.filter(
        Q(counselor=request.user) | Q(user=request.user),
        date__gte=today,
        status=AppointmentStatus.APPROVED
    )
    
    # Get past appointments (past date or completed/cancelled status)
    past_query = Appointment.objects.filter(
        Q(counselor=request.user) | Q(user=request.user)
    ).filter(
        Q(date__lt=today) | 
        Q(status=AppointmentStatus.COMPLETED) | 
        Q(status=AppointmentStatus.CANCELLED)
    )
    
    # Apply filters
    if status:
        upcoming_query = upcoming_query.filter(status=status)
        past_query = past_query.filter(status=status)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            upcoming_query = upcoming_query.filter(date__gte=date_from_obj)
            past_query = past_query.filter(date__gte=date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            upcoming_query = upcoming_query.filter(date__lte=date_to_obj)
            past_query = past_query.filter(date__lte=date_to_obj)
        except ValueError:
            pass
    
    if search:
        upcoming_query = upcoming_query.filter(
            Q(title__icontains=search) | 
            Q(user__full_name__icontains=search)
        )
        past_query = past_query.filter(
            Q(title__icontains=search) | 
            Q(user__full_name__icontains=search)
        )
    
    # Order the results
    upcoming_query = upcoming_query.order_by('date', 'start_time')
    past_query = past_query.order_by('-date', '-start_time')
    
    # Paginate results
    upcoming_paginator = Paginator(upcoming_query, 10)
    past_paginator = Paginator(past_query, 10)
    
    page_number = request.GET.get('page', 1)
    history_page_number = request.GET.get('history_page', 1)
    
    upcoming_appointments = upcoming_paginator.get_page(page_number)
    past_appointments = past_paginator.get_page(history_page_number)
    
    context = {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'selected_status': status,
        'date_from': date_from,
        'date_to': date_to,
        'search': search
    }
    
    return render(request, 'appointment/history.html', context)

# Feedback views
@login_required
@user_passes_test(is_counselor_or_staff)
def feedback_list(request):
    """View feedback from appointments"""
    feedback_query = AppointmentFeedback.objects.all().order_by('-created_at')
    
    # Filter by rating if specified
    rating = request.GET.get('rating')
    if rating and rating.isdigit():
        feedback_query = feedback_query.filter(rating=int(rating))
    
    # Filter by comment content
    comment = request.GET.get('comment')
    if comment:
        feedback_query = feedback_query.filter(comments__icontains=comment)
    
    # Paginate results
    paginator = Paginator(feedback_query, 10)
    page_number = request.GET.get('page', 1)
    feedback = paginator.get_page(page_number)
    
    # Calculate average rating and statistics
    avg_rating = AppointmentFeedback.objects.aggregate(
        avg_rating=Avg('rating')
    )['avg_rating'] or 0
    
    total_feedback = AppointmentFeedback.objects.count()
    positive_feedback = AppointmentFeedback.objects.filter(rating__gte=4).count()
    negative_feedback = AppointmentFeedback.objects.filter(rating__lte=2).count()
    
    # Calculate percentages
    positive_percentage = round((positive_feedback / total_feedback) * 100) if total_feedback > 0 else 0
    negative_percentage = round((negative_feedback / total_feedback) * 100) if total_feedback > 0 else 0
    
    # Calculate rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        rating_distribution[i] = AppointmentFeedback.objects.filter(rating=i).count()
    
    context = {
        'feedback': feedback,
        'avg_rating': round(avg_rating, 1),
        'total_feedback': total_feedback,
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
        'rating_distribution': rating_distribution,
        'selected_rating': rating,
        'comment_filter': comment
    }
    
    return render(request, 'appointment/feedback.html', context)

# Reports views
@login_required
@user_passes_test(is_counselor_or_staff)
def reports(request):
    """Generate and view appointment reports"""
    today = timezone.now().date()
    report_type = request.GET.get('report_type', 'appointments')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Default date range is last 30 days
    start_date = datetime.strptime(date_from, '%Y-%m-%d').date() if date_from else today - timedelta(days=30)
    end_date = datetime.strptime(date_to, '%Y-%m-%d').date() if date_to else today
            
            # Get appointments in the date range
    appointments = Appointment.objects.filter(
                date__gte=start_date,
                date__lte=end_date
    ).order_by('date', 'start_time')
    
    # Get feedback in the date range
    feedback_list = AppointmentFeedback.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).order_by('-created_at')
    
    # Get blocked slots in the date range
    blocked_slots = BlockedTimeSlot.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date', 'start_time')
    
    # Calculate statistics
    total_appointments = appointments.count()
    completed_appointments = appointments.filter(status=AppointmentStatus.COMPLETED).count()
    cancelled_appointments = appointments.filter(status=AppointmentStatus.CANCELLED).count()
    approved_appointments = appointments.filter(status=AppointmentStatus.APPROVED).count()
    pending_appointments = appointments.filter(status=AppointmentStatus.PENDING).count()
    
    # Calculate average duration
    avg_duration = 0
    if total_appointments > 0:
        total_minutes = 0
        for appointment in appointments:
            start = appointment.start_time
            end = appointment.end_time
            minutes = (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)
            total_minutes += minutes
        avg_duration = total_minutes / total_appointments
    
    # Calculate feedback statistics
    avg_rating = feedback_list.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    total_feedback = feedback_list.count()
    positive_feedback = feedback_list.filter(rating__gte=4).count()
    negative_feedback = feedback_list.filter(rating__lte=2).count()
    positive_percentage = round((positive_feedback / total_feedback) * 100) if total_feedback > 0 else 0
    negative_percentage = round((negative_feedback / total_feedback) * 100) if total_feedback > 0 else 0
    
    # Calculate rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        rating_distribution[i] = feedback_list.filter(rating=i).count()
    
    # Calculate availability statistics
    total_available_hours = 0
    total_blocked_slots = blocked_slots.count()
    total_booked_hours = 0
    booking_rate = 0
    
    # Prepare time-based data
    # Get months between start and end date
    months = []
    current_date = start_date
    time_labels = []
    time_data = []
    
    while current_date <= end_date:
        month_name = current_date.strftime('%b')
        if month_name not in months:
            months.append(month_name)
            
            # Calculate appointments in this month
            month_start = current_date.replace(day=1)
            if current_date.month == 12:
                next_month = current_date.replace(year=current_date.year + 1, month=1, day=1)
        else:
                next_month = current_date.replace(month=current_date.month + 1, day=1)
        month_end = next_month - timedelta(days=1)
            
        appointment_count = Appointment.objects.filter(
                date__gte=month_start,
                date__lte=month_end
            ).count()
            
        time_labels.append(month_name)
        time_data.append(appointment_count)
        
        current_date += timedelta(days=1)
    
    # Prepare feedback over time data
    feedback_count_by_time = []
    avg_rating_by_time = []
    
    for month in months:
        month_obj = datetime.strptime(month, '%b')
        month_number = month_obj.month
        year = today.year
        
        # Check if month is in the future (e.g., Dec when current month is Jan)
        if month_number > today.month:
            year -= 1
            
        month_start = datetime(year, month_number, 1).date()
        if month_number == 12:
            next_month = datetime(year + 1, 1, 1).date()
        else:
            next_month = datetime(year, month_number + 1, 1).date()
        month_end = next_month - timedelta(days=1)
        
        month_feedback = AppointmentFeedback.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end
        )
        
        feedback_count_by_time.append(month_feedback.count())
        avg_month_rating = month_feedback.aggregate(avg=Avg('rating'))['avg'] or 0
        avg_rating_by_time.append(round(avg_month_rating, 1))
    
    # Prepare availability by day data
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    available_hours_by_day = [8, 8, 8, 8, 8, 0, 0]  # Example data
    booked_hours_by_day = [4, 5, 3, 6, 2, 0, 0]     # Example data
    blocked_hours_by_day = [1, 0, 2, 1, 1, 0, 0]    # Example data
    
    # Booking rate over time
    booking_rate_by_time = []
    for i in range(len(time_labels)):
        booking_rate_by_time.append(min(100, random.randint(50, 95)))  # Example data
    
    # Combined stats for template
    stats = {
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'approved_appointments': approved_appointments,
        'pending_appointments': pending_appointments,
        'average_duration': round(avg_duration),
        'average_rating': round(avg_rating, 1),
        'total_feedback': total_feedback,
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
        'total_available_hours': sum(available_hours_by_day),
        'total_blocked_slots': total_blocked_slots,
        'total_booked_hours': sum(booked_hours_by_day),
        'booking_rate': round((sum(booked_hours_by_day) / sum(available_hours_by_day) * 100) if sum(available_hours_by_day) > 0 else 0)
    }
    
    context = {
        'report_type': report_type,
        'date_from': date_from,
        'date_to': date_to,
        'appointments': appointments,
        'feedback_list': feedback_list,
        'blocked_slots': blocked_slots,
        'stats': stats,
        'time_labels': json.dumps(time_labels),
        'time_data': json.dumps(time_data),
        'rating_distribution': rating_distribution,
        'feedback_count_by_time': json.dumps(feedback_count_by_time),
        'avg_rating_by_time': json.dumps(avg_rating_by_time),
        'available_hours_by_day': json.dumps(available_hours_by_day),
        'booked_hours_by_day': json.dumps(booked_hours_by_day),
        'blocked_hours_by_day': json.dumps(blocked_hours_by_day),
        'booking_rate_by_time': json.dumps(booking_rate_by_time)
    }
    
    return render(request, 'appointment/reports.html', context)

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

@login_required
@user_passes_test(is_counselor_or_staff)
def create_appointment(request):
    """Create a new appointment"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.counselor = request.user
            appointment.save()
            
            messages.success(request, 'Appointment created successfully.')
            return redirect('appointment:calendar')
        else:
            messages.error(request, 'There was an error creating the appointment.')
    
    return redirect('appointment:calendar')

@login_required
@user_passes_test(is_counselor_or_staff)
def feedback_detail(request, feedback_id):
    """View detailed feedback information"""
    feedback = get_object_or_404(AppointmentFeedback, id=feedback_id)
    data = {
        'id': feedback.id,
        'rating': feedback.rating,
        'comment': feedback.comment,
        'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M'),
        'appointment': {
            'id': feedback.appointment.id,
            'title': feedback.appointment.title,
            'date': feedback.appointment.date.strftime('%Y-%m-%d'),
            'start_time': feedback.appointment.start_time.strftime('%H:%M'),
            'end_time': feedback.appointment.end_time.strftime('%H:%M'),
            'user': {
                'id': feedback.appointment.user.id,
                'full_name': feedback.appointment.user.full_name,
                'email': feedback.appointment.user.email,
            }
        }
    }
    return JsonResponse(data)

@login_required
@user_passes_test(is_counselor_or_staff)
def export_csv(request):
    """Export report data to CSV"""
    report_type = request.GET.get('report_type', 'appointments')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    today = timezone.now().date()
    start_date = datetime.strptime(date_from, '%Y-%m-%d').date() if date_from else today - timedelta(days=30)
    end_date = datetime.strptime(date_to, '%Y-%m-%d').date() if date_to else today
    
    if report_type == 'appointments':
        # Export appointments
        appointments = Appointment.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date', 'start_time')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="appointments_{start_date}_to_{end_date}.csv"'
        
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
        
    elif report_type == 'feedback':
        # Export feedback
        feedback_list = AppointmentFeedback.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).order_by('-created_at')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="feedback_{start_date}_to_{end_date}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Appointment', 'User', 'Rating', 'Comment'
        ])
        
        for feedback in feedback_list:
            writer.writerow([
                feedback.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                feedback.appointment.title,
                feedback.appointment.user.full_name,
                feedback.rating,
                feedback.comment
            ])
    
    else:
        # Export availability
        blocked_slots = BlockedTimeSlot.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date', 'start_time')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="availability_{start_date}_to_{end_date}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Start Time', 'End Time', 'Reason', 'Created By'
        ])
        
        for slot in blocked_slots:
            writer.writerow([
                slot.date,
                slot.start_time,
                slot.end_time,
                slot.reason,
                slot.counselor.full_name
            ])
    
    return response

@login_required
@user_passes_test(is_counselor_or_staff)
def edit_appointment(request, appointment_id):
    """Edit an existing appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully.')
            return redirect('appointment:calendar')
        else:
            messages.error(request, 'There was an error updating the appointment.')
    else:
        form = AppointmentForm(instance=appointment)
    
    context = {
        'form': form,
        'appointment': appointment,
    }
    
    return render(request, 'appointment/edit_appointment.html', context)

@login_required
@user_passes_test(is_counselor_or_staff)
def edit_blocked_time(request, blocked_time_id):
    """Edit a blocked time slot"""
    blocked_time = get_object_or_404(BlockedTimeSlot, id=blocked_time_id)
    
    if request.method == 'POST':
        form = BlockedTimeSlotForm(request.POST, instance=blocked_time)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blocked time slot updated successfully.')
            return redirect('appointment:calendar')
        else:
            messages.error(request, 'There was an error updating the blocked time slot.')
    else:
        form = BlockedTimeSlotForm(instance=blocked_time)
    
    context = {
        'form': form,
        'blocked_time': blocked_time,
    }
    
    return render(request, 'appointment/edit_blocked_time.html', context)

@login_required
@user_passes_test(is_counselor_or_staff)
def delete_blocked_time(request, blocked_time_id):
    """Delete a blocked time slot"""
    blocked_time = get_object_or_404(BlockedTimeSlot, id=blocked_time_id)
    
    if request.method == 'POST':
        blocked_time.delete()
        messages.success(request, 'Blocked time slot deleted successfully.')
    
    next_url = request.POST.get('next', 'appointment:calendar')
    return redirect(next_url)

@login_required
@user_passes_test(is_counselor_or_staff)
def available_time_slots(request):
    """API endpoint to get available time slots for a specific date"""
    date_str = request.GET.get('date')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        # If date is invalid, use today
        date = timezone.now().date()
    
    # Get the counselor (current user)
    counselor = request.user
    
    # Get blocked time slots for this date and counselor
    blocked_slots = BlockedTimeSlot.objects.filter(
        date=date,
        counselor=counselor
    )
    
    # Get existing appointments for this date and counselor
    existing_appointments = Appointment.objects.filter(
        date=date,
        counselor=counselor
    ).exclude(status=AppointmentStatus.CANCELLED)
    
    # Generate available time slots
    # Default business hours: 9 AM to 5 PM in 30 minute increments
    available_slots = []
    
    # Start at 9 AM
    start_hour = 9
    # End at 5 PM
    end_hour = 17
    
    for hour in range(start_hour, end_hour):
        for minute in [0, 30]:
            start_time = timezone.datetime.combine(
                date, 
                timezone.time(hour, minute)
            ).time()
            
            # Each slot is 30 minutes
            end_minute = (minute + 30) % 60
            end_hour = hour + 1 if minute + 30 >= 60 else hour
            end_time = timezone.datetime.combine(
                date, 
                timezone.time(end_hour, end_minute)
            ).time()
            
            # Check if this time slot is blocked
            is_blocked = any(
                blocked.start_time <= start_time < blocked.end_time or
                blocked.start_time < end_time <= blocked.end_time or
                (start_time <= blocked.start_time and end_time >= blocked.end_time)
                for blocked in blocked_slots
            )
            
            # Check if there's an existing appointment
            is_booked = any(
                appt.start_time <= start_time < appt.end_time or
                appt.start_time < end_time <= appt.end_time or
                (start_time <= appt.start_time and end_time >= appt.end_time)
                for appt in existing_appointments
            )
            
            # Add to available slots if not blocked or booked
            slot = {
                'start_time': start_time.strftime('%H:%M'),
                'end_time': end_time.strftime('%H:%M'),
                'available': not (is_blocked or is_booked)
            }
            
            available_slots.append(slot)
    
    return JsonResponse(available_slots, safe=False)
