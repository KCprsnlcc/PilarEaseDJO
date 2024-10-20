# itrc_tools/views.py

import csv
from django.urls import reverse_lazy
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView  # Import LogoutView
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models.functions import TruncDate
from django.db.models import Q, Count, Avg, Case, When, Value, DurationField
from django.views.decorators.http import require_POST
import tablib
from import_export.formats.base_formats import CSV
from .models import (
    VerificationRequest,
    EnrollmentMasterlist,
    SystemSetting,
    AuditLog,
    CustomUser,
    SessionLog,
    APIPerformanceLog,
    ErrorLog,
    SystemDowntime,
    PageViewLog,
    FeatureUtilizationLog,
    Feedback
)
from django.contrib.auth import get_user_model
from django.db import models
from .forms import SystemSettingForm
from main.models import CustomUser  
from .resources import EnrollmentMasterlistResource
from .forms import SystemSettingForm
from django.db.models.functions import TruncDay
from datetime import datetime, timedelta
import json
from collections import Counter
import string
from wordcloud import WordCloud

# Existing functions and classes (ItrcLoginView, ItrcLogoutView, etc.)

def is_itrc_staff(user):
    return user.is_authenticated and user.is_itrc_staff

class ItrcLoginView(LoginView):
    """
    Custom Login View for ITRC Tools
    """
    template_name = 'itrc_tools/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('itrc_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Successfully logged in.")
        # Log the login event
        AuditLog.objects.create(
            user=self.request.user,
            action='login',
            details=f"User {self.request.user.username} logged in.",
            timestamp=timezone.now()
        )
        return response

class ItrcLogoutView(LogoutView):
    """
    Custom Logout View for ITRC Tools
    Adds a success message upon logout.
    """
    next_page = reverse_lazy('itrc_login')  # Redirect to login page after logout

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Successfully logged out.")
        # Log the logout event
        if request.user.is_authenticated:
            AuditLog.objects.create(
                user=request.user,
                action='logout',
                details=f"User {request.user.username} logged out.",
                timestamp=timezone.now()
            )
        return super().dispatch(request, *args, **kwargs)

@user_passes_test(is_itrc_staff)
@login_required
def itrc_dashboard(request):
    """
    Display key statistics and pending verification requests.
    """
    pending_requests = VerificationRequest.objects.filter(status='pending').select_related('user')
    total_requests = VerificationRequest.objects.count()
    verified_requests = VerificationRequest.objects.filter(status='verified').count()
    rejected_requests = VerificationRequest.objects.filter(status='rejected').count()

    context = {
        'pending_requests': pending_requests,
        'total_requests': total_requests,
        'verified_requests': verified_requests,
        'rejected_requests': rejected_requests,
    }
    return render(request, 'itrc_tools/itrc_dashboard.html', context)

@user_passes_test(is_itrc_staff)
@login_required
def verify_user(request, user_id):
    """
    Approve or reject a user's verification request.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    verification_request = get_object_or_404(VerificationRequest, user=user)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '').strip()

        if action == 'approve':
            user.is_active = True
            user.is_verified = True
            user.verification_status = 'verified'
            user.save()

            verification_request.status = 'verified'
            verification_request.remarks = remarks
            verification_request.save()

            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='verify',
                details=f"Approved user {user.username}. Remarks: {remarks}"
            )

            messages.success(request, f'User {user.username} has been verified.')
        elif action == 'reject':
            user.is_active = False
            user.is_verified = False
            user.verification_status = 'rejected'
            user.save()

            verification_request.status = 'rejected'
            verification_request.remarks = remarks
            verification_request.save()

            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='reject',
                details=f"Rejected user {user.username}. Remarks: {remarks}"
            )

            messages.info(request, f'User {user.username} has been rejected.')
        else:
            messages.error(request, 'Invalid action.')

        return redirect('itrc_dashboard')

    context = {
        'user_obj': user,
        'verification_request': verification_request,
    }
    return render(request, 'itrc_tools/verify_user.html', context)

@user_passes_test(is_itrc_staff)
@login_required
def upload_masterlist(request):
    """
    Upload and process the enrollment masterlist CSV file using django-import-export.
    Display the masterlist data in a table.
    """
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'csv_file' not in request.FILES:
            messages.error(request, 'No file was uploaded.')
            return redirect('upload_masterlist')

        csv_file = request.FILES['csv_file']

        # Ensure the file is a CSV
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file with a .csv extension.')
            return redirect('upload_masterlist')

        try:
            dataset = tablib.Dataset().load(csv_file.read().decode('utf-8'), format='csv', headers=True)

            # Create a resource instance
            resource = EnrollmentMasterlistResource()

            # Perform import
            with transaction.atomic():
                result = resource.import_data(dataset, dry_run=True)  # Dry run to test for errors

                if result.has_errors():
                    # Collect errors and display them
                    error_messages = []
                    for row in result.invalid_rows:
                        error = row.error
                        row_index = row.number
                        error_messages.append(f"Row {row_index}: {error}")

                    messages.error(request, 'There were errors in the uploaded file:')
                    for error_message in error_messages:
                        messages.error(request, error_message)
                    return redirect('upload_masterlist')

                # No errors, perform the actual import
                resource.import_data(dataset, dry_run=False)

            records_processed = len(dataset)
            messages.success(request, f'Successfully imported {records_processed} records.')

            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='upload_masterlist',
                details=f"Uploaded masterlist with {records_processed} records."
            )
            return redirect('upload_masterlist')  # Redirect back to display the data

        except Exception as e:
            messages.error(request, f'An error occurred while processing the file: {e}')
            return redirect('upload_masterlist')
    else:
        search_query = request.GET.get('search', '').strip()

        # Fetch and filter data from EnrollmentMasterlist
        if search_query:
            masterlist_data = EnrollmentMasterlist.objects.filter(
                Q(student_id__icontains=search_query) |
                Q(full_name__icontains=search_query) |
                Q(academic_year_level__icontains=search_query)
            ).order_by('student_id')
        else:
            masterlist_data = EnrollmentMasterlist.objects.all().order_by('student_id')

        # Paginate the results
        paginator = Paginator(masterlist_data, 10)  # Show 10 records per page
        page_number = request.GET.get('page')
        masterlist_page_obj = paginator.get_page(page_number)

        context = {
            'masterlist_data': masterlist_page_obj,
            'masterlist_page_range': paginator.get_elided_page_range(masterlist_page_obj.number, on_each_side=2, on_ends=1),
            'masterlist_page_obj': masterlist_page_obj,
            'search_query': search_query,  # Pass search query back to the template
        }
        return render(request, 'itrc_tools/upload_masterlist.html', context)

@user_passes_test(is_itrc_staff)
@login_required
def manage_users(request):
    """
    Display and manage user accounts, including ITRC staff, counselors, and regular users.
    Handles GET requests for displaying users.
    """
    search_query = request.GET.get('search', '').strip()

    # Search functionality
    if search_query:
        users = CustomUser.objects.filter(
            Q(username__icontains=search_query) |
            Q(student_id__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    else:
        # Fetch all users including verified and not verified
        users = CustomUser.objects.all()

    # Order the users (newest first)
    users = users.order_by('-id')

    # Pagination: Show 10 users per page
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Generate the page range for pagination (similar to logs_page_range)
    users_page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)

    context = {
        'users': page_obj,
        'search_query': search_query,
        'users_page_range': users_page_range,
    }
    return render(request, 'itrc_tools/manage_users.html', context)

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def activate_user(request, user_id):
    """
    Activate and verify a user account via AJAX.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_itrc_staff or user.is_counselor:
        return JsonResponse({'success': False, 'message': 'Cannot activate ITRC staff or counselors.'}, status=400)

    user.is_active = True
    user.is_verified = True
    user.verification_status = 'verified'
    user.save()

    # Log the action
    AuditLog.objects.create(
        user=request.user,
        action='activate',
        details=f"Activated and verified user {user.username}."
    )

    return JsonResponse({'success': True, 'message': f'User {user.username} has been activated and verified.'})

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def deactivate_user(request, user_id):
    """
    Deactivate a user account via AJAX.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_itrc_staff or user.is_counselor:
        return JsonResponse({'success': False, 'message': 'Cannot deactivate ITRC staff or counselors.'}, status=400)

    user.is_active = False
    user.is_verified = False
    user.verification_status = 'deactivated'  # Updated status
    user.save()

    # Log the action
    AuditLog.objects.create(
        user=request.user,
        action='deactivate',
        details=f"Deactivated user {user.username}."
    )

    return JsonResponse({'success': True, 'message': f'User {user.username} has been deactivated.'})

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def delete_user(request, user_id):
    """
    Delete a user account via AJAX.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    username = user.username

    # Prevent deletion of ITRC staff and counselors
    if user.is_itrc_staff or user.is_counselor:
        return JsonResponse({'success': False, 'message': 'Cannot delete ITRC staff or counselors.'}, status=400)

    user.delete()

    # Log the action
    AuditLog.objects.create(
        user=request.user,
        action='delete_user',
        details=f"Deleted user {username}."
    )

    return JsonResponse({'success': True, 'message': f'User {username} has been deleted.'})

@user_passes_test(is_itrc_staff)
@login_required
def system_settings(request):
    """
    View and update system settings.
    """
    settings_qs = SystemSetting.objects.all()

    if request.method == 'POST':
        form = SystemSettingForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']
            value = form.cleaned_data['value']
            setting, created = SystemSetting.objects.update_or_create(
                key=key,
                defaults={'value': value}
            )
            if created:
                messages.success(request, f'System setting "{key}" has been created.')
                action = 'create_setting'
            else:
                messages.success(request, f'System setting "{key}" has been updated.')
                action = 'update_setting'

            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action=action,
                details=f"Set {key} to {value}."
            )

            return redirect('system_settings')
        else:
            messages.error(request, 'There was an error with the form. Please check the fields.')
    else:
        form = SystemSettingForm()

    context = {
        'settings': settings_qs,
        'form': form,
    }
    return render(request, 'itrc_tools/system_settings.html', context)

@user_passes_test(is_itrc_staff)
@login_required
def generate_reports(request):
    """
    Generate and display audit logs and other reports.
    """
    audit_logs = AuditLog.objects.all().order_by('-timestamp')

    # Define the time range (last 30 days)
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)

    # -------------------------
    # 1. User Activity Metrics
    # -------------------------

    # Generate a list of the last 30 days
    date_list = [thirty_days_ago + timedelta(days=x) for x in range(0, 31)]

    # Login Activity: Number of logins per day
    login_activity_qs = (
        SessionLog.objects.filter(session_start__date__gte=thirty_days_ago)
        .annotate(date=TruncDate('session_start'))
        .values('date')
        .annotate(logins=Count('id'))
        .order_by('date')
    )
    login_activity_dict = {entry['date']: entry['logins'] for entry in login_activity_qs}

    login_activity_labels = [date.strftime('%Y-%m-%d') for date in date_list]
    login_activity_counts = [login_activity_dict.get(date, 0) for date in date_list]

    # Daily Active Users (DAU): Number of unique users per day
    dau_qs = (
        SessionLog.objects.filter(session_start__date__gte=thirty_days_ago)
        .annotate(date=TruncDate('session_start'))
        .values('date')
        .annotate(dau=Count('user', distinct=True))
        .order_by('date')
    )
    dau_dict = {entry['date']: entry['dau'] for entry in dau_qs}

    dau_labels = [date.strftime('%Y-%m-%d') for date in date_list]
    dau_counts = [dau_dict.get(date, 0) for date in date_list]

    # User Registrations: Number of new users per day
    CustomUser = get_user_model()
    user_reg_qs = (
        CustomUser.objects.filter(date_joined__date__gte=thirty_days_ago)
        .annotate(date=TruncDate('date_joined'))
        .values('date')
        .annotate(registrations=Count('id'))
        .order_by('date')
    )
    user_reg_dict = {entry['date']: entry['registrations'] for entry in user_reg_qs}

    user_registration_labels = [date.strftime('%Y-%m-%d') for date in date_list]
    user_registration_counts = [user_reg_dict.get(date, 0) for date in date_list]

    # Average Session Duration per User
    average_session_duration = (
        SessionLog.objects.filter(session_end__isnull=False)
        .annotate(duration=Case(
            When(session_end__isnull=False, then=models.F('session_end') - models.F('session_start')),
            default=Value(timedelta()),
            output_field=DurationField(),
        ))
        .aggregate(avg_duration=Avg('duration'))
    )
    avg_session_duration_seconds = average_session_duration['avg_duration'].total_seconds() if average_session_duration['avg_duration'] else 0

    # Check if data exists
    if not any(login_activity_counts):
        messages.warning(request, "No login activity data available for the last 30 days.")

    if not any(dau_counts):
        messages.warning(request, "No Daily Active Users data available for the last 30 days.")

    if not any(user_registration_counts):
        messages.warning(request, "No user registration data available for the last 30 days.")

    # -----------------------------
    # 2. System Performance Metrics
    # -----------------------------

    # API Response Time Analysis
    api_response_time = (
        APIPerformanceLog.objects.filter(timestamp__gte=thirty_days_ago, timestamp__isnull=False)
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(avg_response_time=Avg('response_time'))
        .order_by('date')
    )
    api_response_time_labels = [
        entry['date'].strftime('%Y-%m-%d') 
        for entry in api_response_time 
        if entry['date'] is not None
    ]
    api_response_time_avg = [round(entry['avg_response_time'], 2) for entry in api_response_time if entry['date'] is not None]

    # Error Rates
    error_rates = (
        ErrorLog.objects.filter(timestamp__gte=thirty_days_ago, timestamp__isnull=False)
        .values('error_type', 'timestamp__date')
        .annotate(count=Count('id'))
        .order_by('timestamp__date')
    )
    # Structure error rates as a list of dictionaries with date and counts per error type
    error_rate_data = {}
    for entry in error_rates:
        if entry['timestamp__date'] is None:
            continue  # Skip entries with null dates
        date_str = entry['timestamp__date'].strftime('%Y-%m-%d')
        error_type = entry['error_type']
        count = entry['count']
        if date_str not in error_rate_data:
            error_rate_data[date_str] = {}
        error_rate_data[date_str][error_type] = count

    error_rate_labels = sorted(error_rate_data.keys())
    error_types = ErrorLog.ERROR_TYPE_CHOICES
    error_type_labels = [choice[1] for choice in error_types]

    # Prepare data for stacked bar chart
    error_rate_chart_data = {etype: [] for etype in error_type_labels}
    for date in error_rate_labels:
        for etype in error_type_labels:
            error_rate_chart_data[etype].append(error_rate_data[date].get(etype, 0))

    # System Downtime
    system_downtimes = SystemDowntime.objects.filter(end_time__isnull=True)
    ongoing_downtime = system_downtimes.exists()
    latest_downtime = system_downtimes.first() if ongoing_downtime else None

    # ----------------------------
    # 3. User Feedback Analysis
    # ----------------------------

    # Sentiment Analysis
    feedback_data = Feedback.objects.all().annotate(
        sentiment_category=Case(
            When(sentiment_score__gt=0.1, then=Value('Positive')),
            When(sentiment_score__lt=-0.1, then=Value('Negative')),
            default=Value('Neutral'),
            output_field=models.CharField(),
        )
    )

    feedback_counts = feedback_data.values('sentiment_category').annotate(count=Count('id'))

    sentiment_labels = [entry['sentiment_category'] for entry in feedback_counts]
    sentiment_counts = [entry['count'] for entry in feedback_counts]

    # Top Feedback Keywords
    # Collect all feedback messages
    all_feedback_messages = Feedback.objects.values_list('message', flat=True)

    # Concatenate all messages
    all_text = ' '.join(all_feedback_messages)

    # Remove punctuation and make lowercase
    translator = str.maketrans('', '', string.punctuation)
    all_text = all_text.translate(translator).lower()

    # Split into words
    words = all_text.split()

    # Remove stopwords
    stopwords = set([
        'the', 'and', 'to', 'of', 'a', 'in', 'it', 'is', 'that', 'i',
        'this', 'for', 'with', 'was', 'on', 'but', 'are', 'not', 'have',
        'as', 'be', 'you', 'at', 'or', 'so', 'we', 'if', 'an', 'my',
        'they', 'your', 'can', 'from', 'me', 'all', 'just', 'about',
        'do', 'no', 'us', 'what', 'there', 'their', 'our', 'more', 'like',
        'please', 'other', 'not', 'any', 'some', 'yourself',
    ])

    # Filter words
    filtered_words = [word for word in words if word not in stopwords]

    # Count words
    word_counts = Counter(filtered_words)

    # Get top 20 words
    top_words = word_counts.most_common(20)

    keywords = [word for word, count in top_words]
    keyword_counts = [count for word, count in top_words]

    # ----------------------------
    # 4. Usage Statistics
    # ----------------------------

    # Page Views
    page_views = (
        PageViewLog.objects.filter(timestamp__gte=thirty_days_ago, timestamp__isnull=False)
        .values('page')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]  # Top 10 most viewed pages
    )
    page_view_labels = [entry['page'] for entry in page_views]
    page_view_counts = [entry['count'] for entry in page_views]

    # Feature Utilization
    feature_utilizations = (
        FeatureUtilizationLog.objects.filter(last_used__gte=thirty_days_ago, last_used__isnull=False)
        .values('feature_name')
        .annotate(total_usage=Count('id'))
        .order_by('-total_usage')[:10]  # Top 10 most used features
    )
    feature_utilization_labels = [entry['feature_name'] for entry in feature_utilizations]
    feature_utilization_counts = [entry['total_usage'] for entry in feature_utilizations]

    # ----------------------------
    # 5. Data Volume Metrics
    # ----------------------------

    # Masterlist Uploads Over Time
    masterlist_uploads = (
        AuditLog.objects.filter(action='upload_masterlist', timestamp__gte=thirty_days_ago, timestamp__isnull=False)
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    masterlist_uploads_labels = [
        entry['date'].strftime('%Y-%m-%d') 
        for entry in masterlist_uploads 
        if entry['date'] is not None
    ]
    masterlist_uploads_counts = [entry['count'] for entry in masterlist_uploads if entry['date'] is not None]

    # Data Storage Usage (Assuming file uploads are stored in EnrollmentMasterlist)
    # Replace 'file_size' with your actual field that holds the file size in the EnrollmentMasterlist model
    total_data_storage = EnrollmentMasterlist.objects.aggregate(
        total_size=Count('id') * 100  # Placeholder: replace with actual size calculation
    )['total_size'] or 0  # Size in bytes or adjusted as needed

    # ----------------------------
    # 6. System Notifications & Alerts
    # ----------------------------

    # Notification Delivery Metrics
    # Assuming you have a model to track notification deliveries, replace 'send_notification' with the actual action
    notification_deliveries = (
        AuditLog.objects.filter(action='send_notification', timestamp__gte=thirty_days_ago, timestamp__isnull=False)
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(successful=Count('id'))
        .order_by('date')
    )
    notification_delivery_labels = [
        entry['date'].strftime('%Y-%m-%d') 
        for entry in notification_deliveries 
        if entry['date'] is not None
    ]
    notification_delivery_success = [entry['successful'] for entry in notification_deliveries if entry['date'] is not None]

    # Pending Notifications
    # Assuming you have a related name 'notification' in your CustomUser model pointing to notifications
    # Adjust the related name as per your actual model
    pending_notifications = CustomUser.objects.filter(notification__is_read=False).distinct().count()

    # ----------------------------
    # 7. User Demographic Insights
    # ----------------------------

    # User Role Distribution
    user_roles = CustomUser.objects.values('is_itrc_staff', 'is_counselor').annotate(count=Count('id'))
    role_labels = []
    role_counts = []
    for role in user_roles:
        if role['is_itrc_staff']:
            role_labels.append('ITRC Staff')
        elif role['is_counselor']:
            role_labels.append('Counselor')
        else:
            role_labels.append('User')
        role_counts.append(role['count'])

    # User Verification Status
    user_verification = CustomUser.objects.values('verification_status').annotate(count=Count('id'))
    verification_labels = [entry['verification_status'].capitalize() for entry in user_verification]
    verification_counts = [entry['count'] for entry in user_verification]

    # ----------------------------
    # 8. User Retention Rate (Weekly)
    # ----------------------------

    retention_weeks = 12  # Last 12 weeks
    retention_labels = []
    retention_counts = []
    for i in range(retention_weeks):
        week_start = today - timedelta(weeks=i+1)
        week_end = today - timedelta(weeks=i)
        count = CustomUser.objects.filter(date_joined__range=(week_start, week_end)).count()
        retention_labels.append(week_start.strftime('%b %d'))
        retention_counts.append(count)
    retention_labels.reverse()
    retention_counts.reverse()

    # ----------------------------
    # 9. Compile Context
    # ----------------------------

    context = {
        'audit_logs': audit_logs,

        # User Activity Metrics
        'login_activity_labels': json.dumps(login_activity_labels),
        'login_activity_counts': json.dumps(login_activity_counts),
        'user_registration_labels': json.dumps(user_registration_labels),
        'user_registration_counts': json.dumps(user_registration_counts),
        'dau_labels': json.dumps(dau_labels),
        'dau_counts': json.dumps(dau_counts),
        'avg_session_duration_seconds': avg_session_duration_seconds,

        # System Performance Metrics
        'api_response_time_labels': json.dumps(api_response_time_labels),
        'api_response_time_avg': json.dumps(api_response_time_avg),
        'error_rate_labels': json.dumps(error_type_labels),
        'error_rate_data': json.dumps(error_rate_chart_data),
        'system_downtime': ongoing_downtime,
        'latest_downtime': latest_downtime,

        # User Feedback Analysis
        'sentiment_labels': json.dumps(sentiment_labels),
        'sentiment_counts': json.dumps(sentiment_counts),
        'keywords': json.dumps(keywords),
        'keyword_counts': json.dumps(keyword_counts),

        # Usage Statistics
        'page_view_labels': json.dumps(page_view_labels),
        'page_view_counts': json.dumps(page_view_counts),
        'feature_utilization_labels': json.dumps(feature_utilization_labels),
        'feature_utilization_counts': json.dumps(feature_utilization_counts),

        # Data Volume Metrics
        'masterlist_uploads_labels': json.dumps(masterlist_uploads_labels),
        'masterlist_uploads_counts': json.dumps(masterlist_uploads_counts),
        'total_data_storage': round(total_data_storage / (1024 * 1024), 2),  # Convert to MB (adjust as needed)

        # System Notifications & Alerts
        'notification_delivery_labels': json.dumps(notification_delivery_labels),
        'notification_delivery_success': json.dumps(notification_delivery_success),
        'pending_notifications': pending_notifications,

        # User Demographic Insights
        'role_labels': json.dumps(role_labels),
        'role_counts': json.dumps(role_counts),
        'verification_labels': json.dumps(verification_labels),
        'verification_counts': json.dumps(verification_counts),

        # User Retention Rate
        'retention_labels': json.dumps(retention_labels),
        'retention_counts': json.dumps(retention_counts),
    }

    return render(request, 'itrc_tools/reports.html', context)

@user_passes_test(is_itrc_staff)
@login_required
def audit_logs_view(request):
    """
    Display paginated audit logs with search filtering.
    """
    search_query = request.GET.get('search', '').strip()

    if search_query:
        logs = AuditLog.objects.filter(
            Q(user__username__icontains=search_query) |
            Q(action__icontains=search_query) |
            Q(details__icontains=search_query)
        ).order_by('-timestamp')
    else:
        logs = AuditLog.objects.all().order_by('-timestamp')

    # Pagination: 10 logs per page
    paginator = Paginator(logs, 10)
    page_number = request.GET.get('page')
    logs_page_obj = paginator.get_page(page_number)

    context = {
        'logs': logs_page_obj,
        'search_query': search_query,
        'logs_page_range': paginator.get_elided_page_range(logs_page_obj.number, on_each_side=2, on_ends=1)
    }
    return render(request, 'itrc_tools/auditlog.html', context)

# New View for Bulk Actions
@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def manage_users_bulk_action(request):
    """
    Handle bulk actions for managing users.
    """
    bulk_action = request.POST.get('bulk_action')
    selected_users = request.POST.getlist('selected_users')

    if not bulk_action:
        messages.error(request, 'No bulk action selected.')
        return redirect('manage_users')

    if not selected_users:
        messages.error(request, 'No users selected for the bulk action.')
        return redirect('manage_users')

    # Convert selected_users to integers
    try:
        selected_users = list(map(int, selected_users))
    except ValueError:
        messages.error(request, 'Invalid user selection.')
        return redirect('manage_users')

    # Fetch users excluding ITRC staff and counselors
    users_qs = CustomUser.objects.filter(id__in=selected_users).exclude(Q(is_itrc_staff=True) | Q(is_counselor=True))

    if bulk_action == 'verify':
        updated_count = users_qs.update(is_verified=True, verification_status='verified')
        AuditLog.objects.create(
            user=request.user,
            action='bulk_verify',
            details=f"Bulk verified {updated_count} users."
        )
        messages.success(request, f'Successfully verified {updated_count} users.')

    elif bulk_action == 'activate':
        updated_count = users_qs.update(is_active=True, is_verified=True, verification_status='verified')
        AuditLog.objects.create(
            user=request.user,
            action='bulk_activate',
            details=f"Bulk activated and verified {updated_count} users."
        )
        messages.success(request, f'Successfully activated and verified {updated_count} users.')

    elif bulk_action == 'deactivate':
        updated_count = users_qs.update(is_active=False, is_verified=False, verification_status='deactivated')  # Updated status
        AuditLog.objects.create(
            user=request.user,
            action='bulk_deactivate',
            details=f"Bulk deactivated and rejected {updated_count} users."
        )
        messages.success(request, f'Successfully deactivated and rejected {updated_count} users.')

    elif bulk_action == 'delete':
        # Prevent deletion of ITRC staff and counselors
        non_deletable_users = CustomUser.objects.filter(
            Q(id__in=selected_users) & (Q(is_itrc_staff=True) | Q(is_counselor=True))
        )
        if non_deletable_users.exists():
            messages.error(request, 'Cannot delete ITRC staff or counselors.')
            return redirect('manage_users')

        deleted_count, _ = users_qs.delete()
        AuditLog.objects.create(
            user=request.user,
            action='bulk_delete',
            details=f"Bulk deleted {deleted_count} users."
        )
        messages.success(request, f'Successfully deleted {deleted_count} users.')

    else:
        messages.error(request, 'Invalid bulk action selected.')

    return redirect('manage_users')