from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import plotly.express as px
import io
import csv
from django.urls import reverse_lazy
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView  # Import LogoutView
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models.functions import TruncDate
from django.db.models import Q, Count, Avg, Case, When, Value, DurationField
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import tablib
from import_export.formats.base_formats import CSV
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_GET
from django.db import IntegrityError
from .forms import AddUserForm, EditUserForm, UserProfileForm
from django.http import HttpResponse
from .models import (
    VerificationRequest,
    EnrollmentMasterlist,
    SystemSetting,
    AuditLog,
    SessionLog,
    APIPerformanceLog,
    ErrorLog,
    SystemDowntime,
    PageViewLog,
    FeatureUtilizationLog,
    Feedback,
    Notification_System,
)
from django.contrib.auth import get_user_model
from django.db import models
from .forms import SystemSettingForm
from main.models import CustomUser, UserProfile
from .resources import EnrollmentMasterlistResource
from .forms import SystemSettingForm
from django.db.models.functions import TruncDay
from datetime import datetime, timedelta
import json
from collections import Counter
import string
from wordcloud import WordCloud
import logging
logger = logging.getLogger(__name__)
# Existing functions and classes (ItrcLoginView, ItrcLogoutView, etc.)

def is_itrc_staff(user):
    return user.is_authenticated and user.is_itrc_staff

class ItrcLoginView(LoginView):
    template_name = 'itrc_tools/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('itrc_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        messages.success(self.request, "Successfully logged in.")

        # Log the login event
        AuditLog.objects.create(
            user=user,
            action='login',
            details=f"User {user.username} logged in.",
            timestamp=timezone.now()
        )

        # Process pending verification request
        if user.verification_status == 'pending':
            verification_request = VerificationRequest.objects.get(user=user)
            if SystemSetting.is_auto_accept_enabled():
                verification_request.auto_accept()
                messages.success(self.request, f'User {user.username} has been automatically verified.')
            elif SystemSetting.is_auto_reject_enabled():
                verification_request.auto_reject()
                messages.info(self.request, f'User {user.username} has been automatically rejected.')

        return response

    def auto_accept_user(self, user):
        user.is_active = True
        user.is_verified = True
        user.verification_status = 'verified'
        user.save()

        verification_request = get_object_or_404(VerificationRequest, user=user)
        verification_request.status = 'verified'
        verification_request.remarks = 'Auto-verified by system.'
        verification_request.save()

        # Log the action
        AuditLog.objects.create(
            user=self.request.user,
            action='verify',
            details=f"Auto-approved user {user.username}.",
            timestamp=timezone.now()
        )

        # Send notification to the user
        Notification_System.objects.create(
            user=user,
            notification_type='success',
            message='Your account has been automatically verified by the ITRC staff.',
            link=reverse('itrc_dashboard')  # Adjust as needed
        )

        messages.success(self.request, f'User {user.username} has been automatically verified.')


    def auto_reject_user(self, user):
        user.is_active = False
        user.is_verified = False
        user.verification_status = 'rejected'
        user.save()

        verification_request = get_object_or_404(VerificationRequest, user=user)
        verification_request.status = 'rejected'
        verification_request.remarks = 'Auto-rejected by system.'
        verification_request.save()

        # Log the action
        AuditLog.objects.create(
            user=self.request.user,
            action='reject',
            details=f"Auto-rejected user {user.username}.",
            timestamp=timezone.now()
        )

        # Send notification to the user
        Notification_System.objects.create(
            user=user,
            notification_type='warning',
            message='Your account verification request has been automatically rejected by the ITRC staff.',
            link=reverse('contact_support')  # Adjust as needed
        )

        messages.info(self.request, f'User {user.username} has been automatically rejected.')

@user_passes_test(is_itrc_staff)
@login_required
def fetch_pending_requests(request):
    search_query = request.GET.get('search', '').strip()
    if search_query:
        pending_requests = VerificationRequest.objects.filter(
            status='pending',
            user__student_id__icontains=search_query
        ).select_related('user').order_by('user__id')
    else:
        pending_requests = VerificationRequest.objects.filter(status='pending').select_related('user').order_by('user__id')
    
    pending_list = []
    for req in pending_requests:
        pending_list.append({
            'user_id': req.user.id,
            'student_id': req.user.student_id,
            'username': req.user.username,
            'submitted_at': req.submitted_at.strftime('%Y-%m-%d %H:%M'),
        })
    
    # Log the action
    AuditLog.objects.create(
        user=request.user,
        action='fetch_pending_requests',
        details=f"Fetched pending requests with search query: '{search_query}'.",
        timestamp=timezone.now()
    )
    # Notify ITRC staff
    message = f"{request.user.username} fetched pending verification requests."
    link = reverse('itrc_dashboard')  # Adjust as needed
    notify_itrc_staff('info', message, link)

    return JsonResponse({'pending_requests': pending_list})
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
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        pending_requests = VerificationRequest.objects.filter(
            status='pending',
            user__student_id__icontains=search_query
        ).select_related('user').order_by('user__id')
    else:
        pending_requests = VerificationRequest.objects.filter(status='pending').select_related('user').order_by('user__id')
    
    # Pagination setup
    paginator = Paginator(pending_requests, 10)  # Show 10 requests per page
    page_number = request.GET.get('page')
    pending_requests_page = paginator.get_page(page_number)
    
    total_requests = VerificationRequest.objects.count()
    verified_requests = VerificationRequest.objects.filter(
        Q(status='verified') | Q(status='auto_accepted')
    ).count()
    rejected_requests = VerificationRequest.objects.filter(
        Q(status='rejected') | Q(status='auto_rejected')
    ).count()
    
    # Additional Statistics
    auto_accepted_requests = VerificationRequest.objects.filter(status='auto_accepted').count()
    auto_rejected_requests = VerificationRequest.objects.filter(status='auto_rejected').count()
    pending_auto_actions = VerificationRequest.objects.filter(status='pending').count()  # Set for all pending

    
    # Fetch auto settings
    auto_accept_enabled = SystemSetting.get_setting('auto_accept_enabled', 'false') == 'true'
    auto_reject_enabled = SystemSetting.get_setting('auto_reject_enabled', 'false') == 'true'
    elided_page_range = paginator.get_elided_page_range(pending_requests_page.number, on_each_side=2, on_ends=1)
    context = {
        'pending_requests': pending_requests_page,  # Pass the Page object
        'total_requests': total_requests,
        'verified_requests': verified_requests,
        'rejected_requests': rejected_requests,
        'auto_accepted_requests': auto_accepted_requests,
        'auto_rejected_requests': auto_rejected_requests,
        'pending_auto_actions': pending_auto_actions,
        'auto_accept_enabled': 'true' if auto_accept_enabled else 'false',
        'auto_reject_enabled': 'true' if auto_reject_enabled else 'false',
        'elided_page_range': elided_page_range,
        'search_query': search_query,  # To preserve the search query in the template
    }


    return render(request, 'itrc_tools/itrc_dashboard.html', context)

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def auto_accept_all(request):
    pending_requests = VerificationRequest.objects.filter(status='pending').select_related('user')
    if not pending_requests.exists():
        messages.info(request, "No pending verification requests to accept.")
        return redirect('itrc_dashboard')

    for request in pending_requests:
        request.auto_accept()
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='verify',
            details=f"Auto-approved user {request.user.username}.",
            timestamp=timezone.now()
        )

    messages.success(request, f"Successfully auto-accepted {pending_requests.count()} verification requests.")
    return redirect('itrc_dashboard')

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def toggle_auto_reject(request):
    enabled = request.POST.get('enabled') == 'true'
    try:
        # Update the setting
        SystemSetting.set_setting('auto_reject_enabled', 'true' if enabled else 'false')
        if enabled:
            # Disable auto_accept
            SystemSetting.set_setting('auto_accept_enabled', 'false')

            # Process all pending requests
            pending_requests = VerificationRequest.objects.filter(status='pending').select_related('user')
            for verification_request in pending_requests:
                verification_request.auto_reject()
                # Log the action
                AuditLog.objects.create(
                    user=request.user,
                    action='reject',
                    details=f"Auto-rejected user {verification_request.user.username}.",
                    timestamp=timezone.now()
                )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
def is_auto_accept_enabled():
    return SystemSetting.get_setting('auto_accept_enabled', 'false') == 'true'

def is_auto_reject_enabled():
    return SystemSetting.get_setting('auto_reject_enabled', 'false') == 'true'

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def toggle_auto_accept(request):
    enabled = request.POST.get('enabled') == 'true'
    try:
        # Update the setting
        SystemSetting.set_setting('auto_accept_enabled', 'true' if enabled else 'false')
        if enabled:
            # Disable auto_reject and process all pending requests for auto-accept
            SystemSetting.set_setting('auto_reject_enabled', 'false')
            pending_requests = VerificationRequest.objects.filter(status='pending').select_related('user')
            for verification_request in pending_requests:
                verification_request.auto_accept()
        elif not SystemSetting.get_setting('auto_reject_enabled', 'false') == 'true':
            # When both are disabled
            pending_requests = VerificationRequest.objects.filter(status='pending').select_related('user')
            for verification_request in pending_requests:
                user = verification_request.user
                user.is_active = True
                user.is_verified = False
                user.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def toggle_auto_reject(request):
    enabled = request.POST.get('enabled') == 'true'
    try:
        # Update the setting
        SystemSetting.set_setting('auto_reject_enabled', 'true' if enabled else 'false')
        if enabled:
            # Disable auto_accept and process all pending requests for auto-reject
            SystemSetting.set_setting('auto_accept_enabled', 'false')
            pending_requests = VerificationRequest.objects.filter(status='pending').select_related('user')
            for verification_request in pending_requests:
                verification_request.auto_reject()
        elif not SystemSetting.get_setting('auto_accept_enabled', 'false') == 'true':
            # When both are disabled
            pending_requests = VerificationRequest.objects.filter(status='pending').select_related('user')
            for verification_request in pending_requests:
                user = verification_request.user
                user.is_active = True
                user.is_verified = False
                user.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def manual_accept_user(request, user_id):
    """
    Manually accept a user via AJAX.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    verification_request = get_object_or_404(VerificationRequest, user=user, status='pending')

    try:
        with transaction.atomic():
            user.is_active = True
            user.is_verified = True
            user.verification_status = 'verified'
            user.save()

            verification_request.status = 'verified'
            verification_request.remarks = 'Manually approved by staff.'
            verification_request.save()

            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='verify',
                details=f"Manually approved user {user.username}.",
                timestamp=timezone.now()
            )

            # Send notification to the user
            Notification_System.objects.create(
                user=user,
                notification_type='success',
                message='Your account has been manually verified by the ITRC staff.',
                link=reverse('itrc_dashboard')  # Adjust as needed
            )

        return JsonResponse({'success': True, 'message': f'User {user.username} has been accepted.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred while accepting the user.'}, status=500)

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def manual_reject_user(request, user_id):
    """
    Manually reject a user via AJAX.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    verification_request = get_object_or_404(VerificationRequest, user=user, status='pending')
    remarks = request.POST.get('remarks', '').strip()

    if not remarks:
        return JsonResponse({'success': False, 'message': 'Remarks are required for rejection.'}, status=400)

    try:
        with transaction.atomic():
            user.is_active = True
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
                details=f"Manually rejected user {user.username}. Remarks: {remarks}",
                timestamp=timezone.now()
            )

            # Send notification to the user
            Notification_System.objects.create(
                user=user,
                notification_type='warning',
                message='Your account verification request has been manually rejected by the ITRC staff.',
                link=reverse('contact_support')  # Adjust as needed
            )

        return JsonResponse({'success': True, 'message': f'User {user.username} has been rejected.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred while rejecting the user.'}, status=500)
@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def auto_reject_all(request):
    pending_requests = VerificationRequest.objects.filter(status='pending').select_related('user')
    if not pending_requests.exists():
        messages.info(request, "No pending verification requests to reject.")
        return redirect('itrc_dashboard')

    for request in pending_requests:
        request.auto_reject()
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='reject',
            details=f"Auto-rejected user {request.user.username}.",
            timestamp=timezone.now()
        )

    messages.success(request, f"Successfully auto-rejected {pending_requests.count()} verification requests.")
    return redirect('itrc_dashboard')

@user_passes_test(is_itrc_staff)
@login_required
def verify_user(request, user_id):
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
                details=f"Approved user {user.username}. Remarks: {remarks}",
                timestamp=timezone.now()
            )

            # Send notification to the user
            Notification_System.objects.create(
                user=user,
                notification_type='success',
                message='Your account has been verified by the ITRC staff.',
                link=reverse('itrc_dashboard')  # Adjust as needed
            )

            messages.success(request, f'User {user.username} has been verified.')
        elif action == 'reject':
            user.is_active = True
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
                details=f"Rejected user {user.username}. Remarks: {remarks}",
                timestamp=timezone.now()
            )

            # Send notification to the user
            Notification_System.objects.create(
                user=user,
                notification_type='warning',
                message='Your account verification request has been rejected by the ITRC staff.',
                link=reverse('contact_support')  # Adjust as needed
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
                details=f"Uploaded masterlist with {records_processed} records.",
                timestamp=timezone.now()
            )

            # Send notification to all ITRC staff
            message = f"{request.user.username} uploaded a masterlist with {records_processed} records."
            link = reverse('upload_masterlist')  # Adjust as needed
            notify_itrc_staff('info', message, link)

            return redirect('upload_masterlist') # Redirect back to display the data

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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@require_GET
@login_required
def fetch_notifications(request):
    page_number = request.GET.get('page', 1)
    notifications = []

    seven_weeks_ago = timezone.now() - timedelta(weeks=7)
    user_notifications = Notification_System.objects.filter(
        user=request.user,
        timestamp__gte=seven_weeks_ago
    ).order_by('-timestamp')

    paginator = Paginator(user_notifications, 5)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    for notification in page_obj.object_list:
        notifications.append({
            'id': notification.id,
            'message': notification.message,
            'link': notification.link,
            'avatar': notification.user.profile.avatar.url if notification.user.profile.avatar else '/static/images/avatars/placeholder.png',
            'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M'),
            'is_read': notification.is_read
        })

    AuditLog.objects.create(
        user=request.user,
        action='fetch_notifications',
        details=f"Fetched notifications for user {request.user.username}.",
        timestamp=timezone.now()
    )

    return JsonResponse({
        'notifications': notifications,
        'total_pages': paginator.num_pages
    })

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
    search_query = request.GET.get('search', '').strip()

    if search_query:
        users = CustomUser.objects.filter(
            Q(username__icontains=search_query) |
            Q(student_id__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    else:
        users = CustomUser.objects.all()

    users = users.order_by('-id')
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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
    user = get_object_or_404(CustomUser, id=user_id)
    
    # **Prevent activating own account if necessary**
    if user == request.user:
        return JsonResponse({'success': False, 'message': 'You cannot activate your own account.'}, status=400)
    
    user.is_active = True
    user.is_verified = True
    user.verification_status = 'verified'
    user.save()

    # Log the action
    AuditLog.objects.create(
        user=request.user,
        action='activate',
        details=f"Activated and verified user {user.username}.",
        timestamp=timezone.now()
    )

    # Send notification to all ITRC staff
    message = f"User '{user.username}' has been activated and verified by {request.user.username}."
    link = reverse('manage_users')  # Adjust as needed
    notify_itrc_staff(request, 'success', message, link)

    return JsonResponse({'success': True, 'message': f'User {user.username} has been activated and verified.'})
@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    # **Prevent deactivating own account if necessary**
    if user == request.user:
        return JsonResponse({'success': False, 'message': 'You cannot deactivate your own account.'}, status=400)
    
    user.is_active = False
    user.is_verified = False
    user.verification_status = 'deactivated'
    user.save()

    # Log the action
    AuditLog.objects.create(
        user=request.user,
        action='deactivate',
        details=f"Deactivated user {user.username}.",
        timestamp=timezone.now()
    )

    # Send notification to all ITRC staff
    message = f"User '{user.username}' has been deactivated by {request.user.username}."
    link = reverse('manage_users')  # Adjust as needed
    notify_itrc_staff(request, 'warning', message, link)


    return JsonResponse({'success': True, 'message': f'User {user.username} has been deactivated.'})

def contact_support(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not subject or not message:
            messages.error(request, 'Both subject and message are required.')
            return redirect('contact_support')

        messages.success(request, 'Your message has been sent to support.')

        AuditLog.objects.create(
            user=request.user,
            action='contact_support',
            details=f"User {request.user.username} contacted support with subject: {subject}",
            timestamp=timezone.now()
        )

        return redirect('itrc_dashboard')

    return render(request, 'itrc_tools/contact_support.html')

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    username = user.username

    # **Prevent deleting own account**
    if user == request.user:
        return JsonResponse({'success': False, 'message': 'You cannot delete your own account.'}, status=400)

    user.delete()

    # Log the action
    AuditLog.objects.create(
        user=request.user,
        action='delete_user',
        details=f"Deleted user {username}.",
        timestamp=timezone.now()
    )

    # Send notification to ITRC staff
    message = f"{request.user.username} deleted user: {username}."
    link = reverse('manage_users')
    notify_itrc_staff(request, 'error', message, link)


    return JsonResponse({'success': True, 'message': f'User {username} has been deleted.'})

@user_passes_test(is_itrc_staff)
@login_required
def system_settings(request):
    settings_qs = SystemSetting.objects.all()

    if request.method == 'POST':
        form = SystemSettingForm(request.POST)
        if form.is_valid():
            auto_accept_enabled = form.cleaned_data['auto_accept_enabled']
            auto_reject_enabled = form.cleaned_data['auto_reject_enabled']

            # Update the settings in the database
            SystemSetting.set_setting('auto_accept_enabled', 'true' if auto_accept_enabled else 'false')
            SystemSetting.set_setting('auto_reject_enabled', 'true' if auto_reject_enabled else 'false')

            # Log the action
            action = 'update_setting'
            AuditLog.objects.create(
                user=request.user,
                action=action,
                details=f"Set auto_accept_enabled to {auto_accept_enabled} and auto_reject_enabled to {auto_reject_enabled}.",
                timestamp=timezone.now()
            )

            messages.success(request, 'System settings have been updated successfully.')
            return redirect('system_settings')
        else:
            messages.error(request, 'There was an error with the form. Please check the fields.')
    else:
        # Populate the form with current settings
        initial_data = {
            'auto_accept_enabled': SystemSetting.get_setting('auto_accept_enabled') == 'true',
            'auto_reject_enabled': SystemSetting.get_setting('auto_reject_enabled') == 'true',
        }
        form = SystemSettingForm(initial=initial_data)

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
    notification_deliveries = (
        AuditLog.objects.filter(action='send_notification', timestamp__gte=thirty_days_ago)
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
    notification_delivery_success = [
        entry['successful'] for entry in notification_deliveries if entry['date'] is not None
    ]

    # Pending Notifications
    pending_notifications = Notification_System.objects.filter(is_read=False).count()

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
        
         'notification_delivery_labels': json.dumps(notification_delivery_labels),
        'notification_delivery_success': json.dumps(notification_delivery_success),
        'pending_notifications': pending_notifications,
    }
     # Check if the request is for a PDF download
    if request.GET.get('download') == 'pdf':
        # Create a byte stream buffer
        buffer = io.BytesIO()

        # Set up PDF document using SimpleDocTemplate
        pdf_doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Add a title to the PDF
        elements.append(Paragraph("ITRC Reports", styles['Title']))

        # Section: User Activity Metrics
        elements.append(Paragraph("User Activity Metrics", styles['Heading2']))
        elements.append(Paragraph("Login Activity", styles['Heading3']))

        # Prepare data for tables
        login_activity_data = [["Date", "Logins"]] + list(zip(context['login_activity_labels'], context['login_activity_counts']))
        login_activity_table = Table(login_activity_data)
        login_activity_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(login_activity_table)

        # Other sections (Daily Active Users, User Registrations, etc.) follow similarly
        # Example of adding another section
        elements.append(Paragraph("User Registrations", styles['Heading3']))
        user_registration_data = [["Date", "Registrations"]] + list(zip(context['user_registration_labels'], context['user_registration_counts']))
        user_registration_table = Table(user_registration_data)
        user_registration_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(user_registration_table)

        # Finalize PDF generation
        pdf_doc.build(elements)

        # Get PDF data from buffer
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ITRC_Report.pdf"'
        buffer.close()
        return response

    return render(request, 'itrc_tools/reports.html', context)

@user_passes_test(is_itrc_staff)
@login_required
def generate_pdf_report(request):
    # Define context data for PDF generation as in generate_reports
    # Replace these placeholders with actual data from generate_reports
    context = {
        'login_activity_labels': ["2024-01-01", "2024-01-02", "2024-01-03"],
        'login_activity_counts': [10, 15, 20],
        'user_registration_labels': ["2024-01-01", "2024-01-02", "2024-01-03"],
        'user_registration_counts': [3, 6, 9],
        'dau_labels': ["2024-01-01", "2024-01-02", "2024-01-03"],
        'dau_counts': [5, 8, 10],
        'avg_session_duration_seconds': 300,
        'api_response_time_labels': ["2024-01-01", "2024-01-02", "2024-01-03"],
        'api_response_time_avg': [100, 150, 120],
        'error_rate_labels': ["System Error", "Network Error"],
        'error_rate_data': {"System Error": [1, 2, 3], "Network Error": [2, 1, 0]},
        'system_downtime': False,
        'sentiment_labels': ["Positive", "Neutral", "Negative"],
        'sentiment_counts': [20, 30, 10],
        'keywords': ["service", "feedback", "help"],
        'keyword_counts': [15, 12, 10],
        'page_view_labels': ["Dashboard", "Profile", "Settings"],
        'page_view_counts': [100, 200, 150],
        'feature_utilization_labels': ["Login", "View Profile", "Upload"],
        'feature_utilization_counts': [300, 150, 90],
        'masterlist_uploads_labels': ["2024-01-01", "2024-01-02", "2024-01-03"],
        'masterlist_uploads_counts': [5, 10, 8],
        'total_data_storage': 512.5,
        'notification_delivery_labels': ["2024-01-01", "2024-01-02", "2024-01-03"],
        'notification_delivery_success': [50, 60, 70],
        'role_labels': ["ITRC Staff", "Counselor", "User"],
        'role_counts': [10, 20, 70],
        'verification_labels': ["Verified", "Pending", "Rejected"],
        'verification_counts': [50, 30, 20],
        'retention_labels': ["Week 1", "Week 2", "Week 3"],
        'retention_counts': [12, 10, 8],
    }

    # Create a byte buffer for the PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Add title
    elements.append(Paragraph("ITRC Reports & Analytics", styles['Title']))
    elements.append(Spacer(1, 12))

    # --------------------------
    # 1. User Activity Metrics
    # --------------------------
    elements.append(Paragraph("User Activity Metrics", styles['Heading2']))

    # Login Activity Table
    login_activity_data = [["Date", "Logins"]] + list(zip(context['login_activity_labels'], context['login_activity_counts']))
    elements.append(Paragraph("Login Activity", styles['Heading3']))
    elements.append(Table(login_activity_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Spacer(1, 12))

    # Daily Active Users Table
    dau_data = [["Date", "Active Users"]] + list(zip(context['dau_labels'], context['dau_counts']))
    elements.append(Paragraph("Daily Active Users", styles['Heading3']))
    elements.append(Table(dau_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Spacer(1, 12))

    # -----------------------------
    # 2. System Performance Metrics
    # -----------------------------
    elements.append(Paragraph("System Performance Metrics", styles['Heading2']))

    # API Response Time Table
    api_response_data = [["Date", "Avg Response Time"]] + list(zip(context['api_response_time_labels'], context['api_response_time_avg']))
    elements.append(Paragraph("API Response Times", styles['Heading3']))
    elements.append(Table(api_response_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Spacer(1, 12))

    # Error Rate Table
    error_rate_data = [["Date"] + context['error_rate_labels']]
    for i, date in enumerate(context['api_response_time_labels']):
        row = [date] + [context['error_rate_data'][error][i] for error in context['error_rate_labels']]
        error_rate_data.append(row)
    elements.append(Paragraph("Error Rates", styles['Heading3']))
    elements.append(Table(error_rate_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Spacer(1, 12))

    # --------------------------
    # 3. User Feedback Analysis
    # --------------------------
    elements.append(Paragraph("User Feedback Analysis", styles['Heading2']))

    # Sentiment Counts Table
    sentiment_data = [["Sentiment", "Count"]] + list(zip(context['sentiment_labels'], context['sentiment_counts']))
    elements.append(Paragraph("Sentiment Analysis", styles['Heading3']))
    elements.append(Table(sentiment_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Spacer(1, 12))

    # --------------------------
    # 4. Usage Statistics
    # --------------------------
    elements.append(Paragraph("Usage Statistics", styles['Heading2']))

    # Page Views Table
    page_view_data = [["Page", "Views"]] + list(zip(context['page_view_labels'], context['page_view_counts']))
    elements.append(Paragraph("Page Views", styles['Heading3']))
    elements.append(Table(page_view_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Spacer(1, 12))

    # Feature Utilization Table
    feature_utilization_data = [["Feature", "Usage Count"]] + list(zip(context['feature_utilization_labels'], context['feature_utilization_counts']))
    elements.append(Paragraph("Feature Utilization", styles['Heading3']))
    elements.append(Table(feature_utilization_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Spacer(1, 12))

    # --------------------------
    # 5. Data Volume Metrics
    # --------------------------
    elements.append(Paragraph("Data Volume Metrics", styles['Heading2']))

    # Masterlist Uploads Table
    masterlist_data = [["Date", "Uploads"]] + list(zip(context['masterlist_uploads_labels'], context['masterlist_uploads_counts']))
    elements.append(Paragraph("Masterlist Uploads", styles['Heading3']))
    elements.append(Table(masterlist_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Spacer(1, 12))

    # --------------------------
    # 6. System Notifications & Alerts
    # --------------------------
    elements.append(Paragraph("System Notifications & Alerts", styles['Heading2']))

    # Notification Delivery Table
    notification_data = [["Date", "Success Count"]] + list(zip(context['notification_delivery_labels'], context['notification_delivery_success']))
    elements.append(Paragraph("Notification Deliveries", styles['Heading3']))
    elements.append(Table(notification_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Spacer(1, 12))

    # --------------------------
    # 7. User Demographic Insights
    # --------------------------
    elements.append(Paragraph("User Demographic Insights", styles['Heading2']))

    # Role Distribution Table
    role_data = [["Role", "Count"]] + list(zip(context['role_labels'], context['role_counts']))
    elements.append(Paragraph("User Roles", styles['Heading3']))
    elements.append(Table(role_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Spacer(1, 12))

    # Verification Status Table
    verification_data = [["Status", "Count"]] + list(zip(context['verification_labels'], context['verification_counts']))
    elements.append(Paragraph("User Verification Status", styles['Heading3']))
    elements.append(Table(verification_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Spacer(1, 12))

    # --------------------------
    # 8. User Retention Rate (Weekly)
    # --------------------------
    elements.append(Paragraph("User Retention Rate (Weekly)", styles['Heading2']))

    # Retention Rate Table
    retention_data = [["Week", "Users"]] + list(zip(context['retention_labels'], context['retention_counts']))
    elements.append(Table(retention_data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Finalize PDF
    doc.build(elements)
    
    # Get PDF data from buffer
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ITRC_Report.pdf"'
    buffer.close()
    return response
@user_passes_test(is_itrc_staff)
@login_required
def audit_logs_view(request):
    search_query = request.GET.get('search', '').strip()

    if search_query:
        logs = AuditLog.objects.filter(
            Q(user__username__icontains=search_query) |
            Q(action__icontains=search_query) |
            Q(details__icontains=search_query)
        ).order_by('-timestamp')
    else:
        logs = AuditLog.objects.all().order_by('-timestamp')

    paginator = Paginator(logs, 10)
    page_number = request.GET.get('page')
    logs_page_obj = paginator.get_page(page_number)

    context = {
        'logs': logs_page_obj,
        'search_query': search_query,
        'logs_page_range': paginator.get_elided_page_range(
            logs_page_obj.number, on_each_side=2, on_ends=1
        )
    }
    return render(request, 'itrc_tools/auditlog.html', context)
@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def manage_users_bulk_action(request):
    bulk_action = request.POST.get('bulk_action')
    selected_users = request.POST.getlist('selected_users')

    if not bulk_action:
        return JsonResponse({'success': False, 'message': 'No bulk action selected.'}, status=400)

    if not selected_users:
        return JsonResponse({'success': False, 'message': 'No users selected for the bulk action.'}, status=400)

    try:
        selected_users = list(map(int, selected_users))
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Invalid user selection.'}, status=400)

    # **Removed exclusion of ITRC staff and counselors**
    users_qs = CustomUser.objects.filter(id__in=selected_users)

    # **Prevent bulk actions on self**
    if request.user.id in selected_users:
        return JsonResponse({'success': False, 'message': 'You cannot perform bulk actions on your own account.'}, status=400)

    if bulk_action == 'verify':
        updated_count = users_qs.update(is_verified=True, verification_status='verified')
        AuditLog.objects.create(
            user=request.user,
            action='bulk_verify',
            details=f"Bulk verified {updated_count} users.",
            timestamp=timezone.now()
        )
        message = f'Successfully verified {updated_count} users.'
        notify_itrc_staff(request, 'success', f"{request.user.username} bulk verified {updated_count} users.", reverse('manage_users'))
        return JsonResponse({'success': True, 'message': message})

    elif bulk_action == 'activate':
        updated_count = users_qs.update(is_active=True, is_verified=True, verification_status='verified')
        AuditLog.objects.create(
            user=request.user,
            action='bulk_activate',
            details=f"Bulk activated and verified {updated_count} users.",
            timestamp=timezone.now()
        )
        message = f'Successfully activated and verified {updated_count} users.'
        notify_itrc_staff('success', f"{request.user.username} bulk activated and verified {updated_count} users.", reverse('manage_users'))
        return JsonResponse({'success': True, 'message': message})

    elif bulk_action == 'deactivate':
        updated_count = users_qs.update(is_active=False, is_verified=False, verification_status='deactivated')
        AuditLog.objects.create(
            user=request.user,
            action='bulk_deactivate',
            details=f"Bulk deactivated {updated_count} users.",
            timestamp=timezone.now()
        )
        message = f'Successfully deactivated {updated_count} users.'
        notify_itrc_staff(request, 'warning', f"{request.user.username} bulk deactivated {updated_count} users.", reverse('manage_users'))
        return JsonResponse({'success': True, 'message': message})

    elif bulk_action == 'delete':
        # **Allow deletion of any user, including ITRC staff and counselors**
        # **Prevent bulk deletion of self**
        if request.user.id in selected_users:
            return JsonResponse({'success': False, 'message': 'You cannot delete your own account.'}, status=400)

        deleted_count, _ = users_qs.delete()
        AuditLog.objects.create(
            user=request.user,
            action='bulk_delete',
            details=f"Bulk deleted {deleted_count} users.",
            timestamp=timezone.now()
        )
        notify_itrc_staff('error', f"{request.user.username} bulk deleted {deleted_count} users.", reverse('manage_users'))
        message = f'Successfully deleted {deleted_count} users.'
        return JsonResponse({'success': True, 'message': message})

    else:
        return JsonResponse({'success': False, 'message': 'Invalid bulk action selected.'}, status=400)
@login_required
def notifications_view(request):
    user_notifications = request.user.itrc_notifications.all().order_by('-timestamp')
    context = {
        'notifications': user_notifications
    }
    return render(request, 'itrc_tools/notifications.html', context)
@login_required
@require_POST
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification_System, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()

    AuditLog.objects.create(
        user=request.user,
        action='mark_notification_as_read',
        details=f"Marked notification {notification_id} as read.",
        timestamp=timezone.now()
    )

    return JsonResponse({'success': True})


@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def mark_all_notifications_as_read(request):
    user_notifications = request.user.itrc_notifications.filter(is_read=False)
    user_notifications.update(is_read=True)

    AuditLog.objects.create(
        user=request.user,
        action='mark_all_notifications_as_read',
        details=f"Marked all notifications as read for user {request.user.username}.",
        timestamp=timezone.now()
    )

    return JsonResponse({'success': True})

# itrc_tools/views.py
from django.contrib.auth.models import Group
def notify_itrc_staff(notification_type, message, link=None):
    itrc_staff = CustomUser.objects.filter(is_itrc_staff=True)
    notifications = [
        Notification_System(
            user=staff,
            notification_type=notification_type,
            message=message,
            link=link
        ) for staff in itrc_staff
    ]
    Notification_System.objects.bulk_create(notifications)
    # Log the notification event
    AuditLog.objects.create(
        user=None,
        action='notify_itrc_staff',
        details=f"Sent '{notification_type}' notifications to all ITRC staff.",
        timestamp=timezone.now()
    )

def notify_itrc_staff(request, notification_type, message, link=None):
    itrc_staff = CustomUser.objects.filter(is_itrc_staff=True)
    notifications = [
        Notification_System(
            user=staff,
            notification_type=notification_type,
            message=message,
            link=link
        ) for staff in itrc_staff
    ]
    Notification_System.objects.bulk_create(notifications)
    # Log the notification event with the requesting user
    AuditLog.objects.create(
        user=request.user,
        action='notify_itrc_staff',
        details=f"Sent '{notification_type}' notifications to all ITRC staff.",
        timestamp=timezone.now()
    )
@user_passes_test(is_itrc_staff)
@login_required
@require_http_methods(["GET", "POST"])
def add_user(request):
    if request.method == 'POST':
        user_form = AddUserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    # Save the user
                    user = user_form.save()

                    # At this point, the signal has already created the UserProfile
                    # Now, update the profile with form data
                    profile = user.profile
                    profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
                    profile_form.save()

                    # Log the action
                    AuditLog.objects.create(
                        user=request.user,
                        action='add_user',
                        details=f"Added new user {user.username}.",
                        timestamp=timezone.now()
                    )

                    # Send notification to ITRC staff
                    message = f"{request.user.username} added a new user: {user.username}."
                    link = reverse('manage_users')
                    notify_itrc_staff(request, 'info', message, link)


                    messages.success(request, f'User "{user.username}" has been added successfully.')
                    return redirect('manage_users')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    messages.error(request, f'A user with that username or email already exists.')
                else:
                    messages.error(request, f'An unexpected error occurred: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = AddUserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'itrc_tools/add_user.html', context)
@csrf_exempt  # Ensure CSRF tokens are handled; alternatively, include CSRF tokens in AJAX requests
@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def check_unique(request):
    """
    AJAX view to check the uniqueness of a given field.
    Expects 'field' and 'value' in POST data.
    """
    field = request.POST.get('field')
    value = request.POST.get('value')

    if field not in ['username', 'email', 'student_id']:
        return JsonResponse({'is_unique': False, 'error': 'Invalid field.'}, status=400)

    exists = CustomUser.objects.filter(**{f"{field}__iexact": value}).exists()
    return JsonResponse({'is_unique': not exists})

@user_passes_test(is_itrc_staff)
@login_required
def edit_user_view(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            try:
                form.save()
                # Log the action
                AuditLog.objects.create(
                    user=request.user,
                    action='update_user',
                    details=f"Edited user {user_obj.username}.",
                    timestamp=timezone.now()
                )
                # Send notification to ITRC staff
                message = f"{request.user.username} edited user: {user_obj.username}."
                link = reverse('manage_users')
                notify_itrc_staff(request, 'info', message, link)


                messages.success(request, f'User "{user_obj.username}" has been updated successfully.')
                return redirect('manage_users')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error(None, "A user with that username, email, or student ID already exists.")
                else:
                    form.add_error(None, f'An unexpected error occurred: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditUserForm(instance=user_obj)
        # Pass original values for validation to JavaScript
        form.fields['username'].widget.attrs.update({'data-original': user_obj.username})
        form.fields['email'].widget.attrs.update({'data-original': user_obj.email})
        form.fields['student_id'].widget.attrs.update({'data-original': user_obj.student_id})

    context = {
        'form': form,
        'user_obj': user_obj,
    }
    return render(request, 'itrc_tools/edit_user.html', context)

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def change_role(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    data = json.loads(request.body)
    new_role = data.get('role')

    if new_role not in ['user', 'counselor', 'itrc_staff']:
        return JsonResponse({'success': False, 'message': 'Invalid role selected.'}, status=400)

    # **Prevent changing own role to avoid self-lockout**
    if user == request.user and new_role != 'itrc_staff':
        return JsonResponse({'success': False, 'message': 'You cannot change your own role to a non-ITRC staff.'}, status=400)

    # Update role flags
    user.is_itrc_staff = new_role == 'itrc_staff'
    user.is_counselor = new_role == 'counselor'
    user.save()

    # Optionally, manage user groups based on role
    if new_role == 'itrc_staff':
        itrc_group, created = Group.objects.get_or_create(name='ITRC Staff')
        user.groups.add(itrc_group)
    elif new_role == 'counselor':
        counselor_group, created = Group.objects.get_or_create(name='Counselors')
        user.groups.add(counselor_group)
    else:
        # Remove from all groups if the role is 'user'
        user.groups.clear()

    # Log the action
    AuditLog.objects.create(
        user=request.user,
        action='change_role',
        details=f"Changed role of user {user.username} to {new_role}.",
        timestamp=timezone.now()
    )
    # Send notification to ITRC staff
    message = f"{request.user.username} changed role of user: {user.username} to {new_role}."
    link = reverse('manage_users')
    notify_itrc_staff(request, 'info', message, link)

    return JsonResponse({'success': True, 'message': f"User role updated to {new_role}."})

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def add_student_to_masterlist(request):
    """
    Add a single student to the enrollment masterlist.
    """
    student_id = request.POST.get('student_id')
    full_name = request.POST.get('full_name')
    academic_year_level = request.POST.get('academic_year_level')
    
    # Validate the input
    if not student_id or not full_name or not academic_year_level:
        messages.error(request, 'All fields are required.')
        return redirect('upload_masterlist')
    
    try:
        # Check if the student already exists
        if EnrollmentMasterlist.objects.filter(student_id=student_id).exists():
            messages.error(request, f'Student with ID {student_id} already exists in the masterlist.')
            return redirect('upload_masterlist')
        
        # Create the new student entry
        EnrollmentMasterlist.objects.create(
            student_id=student_id,
            full_name=full_name,
            academic_year_level=academic_year_level
        )
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='add_student_to_masterlist',
            details=f"Added student {student_id} - {full_name} to the enrollment masterlist."
        )
        
        messages.success(request, f'Successfully added {full_name} to the enrollment masterlist.')
    except Exception as e:
        messages.error(request, f'An error occurred while adding the student: {e}')
    
    return redirect('upload_masterlist')