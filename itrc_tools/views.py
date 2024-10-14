# itrc_tools/views.py

import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.views.decorators.http import require_POST
import tablib
from import_export.formats.base_formats import CSV
from .models import (
    VerificationRequest,
    EnrollmentMasterlist,
    SystemSetting,
    AuditLog,
)
from .forms import SystemSettingForm
from main.models import CustomUser  # Assuming main app contains CustomUser
from .resources import EnrollmentMasterlistResource
from .models import EnrollmentMasterlist, AuditLog
from .forms import SystemSettingForm 

def is_itrc_staff(user):
    return user.is_authenticated and user.is_itrc_staff

class ItrcLoginView(LoginView):
    """
    Custom Login View for ITRC Tools
    """
    template_name = 'itrc_tools/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('itrc_dashboard')

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
        # Fetch data from EnrollmentMasterlist
        masterlist_data = EnrollmentMasterlist.objects.all().order_by('student_id')

        context = {
            'masterlist_data': masterlist_data,
        }
        return render(request, 'itrc_tools/upload_masterlist.html', context)

@user_passes_test(is_itrc_staff)
@login_required
def manage_users(request):
    """
    Display and manage user accounts.
    """
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

    # Exclude ITRC staff and counselors from being managed here
    users = users.exclude(Q(is_itrc_staff=True) | Q(is_counselor=True))

    # Pagination: Show 10 users per page
    paginator = Paginator(users.order_by('-id'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'search_query': search_query,
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
        action='verify',
        details=f"Activated and verified user {user.username}."
    )

    return JsonResponse({'success': True, 'message': f'User {user.username} has been activated and verified.'})

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def deactivate_user(request, user_id):
    """
    Deactivate and reject a user account via AJAX.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_itrc_staff or user.is_counselor:
        return JsonResponse({'success': False, 'message': 'Cannot deactivate ITRC staff or counselors.'}, status=400)

    user.is_active = False
    user.is_verified = False
    user.verification_status = 'rejected'
    user.save()

    # Log the action
    AuditLog.objects.create(
        user=request.user,
        action='reject',
        details=f"Deactivated and rejected user {user.username}."
    )

    return JsonResponse({'success': True, 'message': f'User {user.username} has been deactivated and rejected.'})

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

    # Implement filtering based on GET parameters if needed
    # For example, filter by user, action, date range, etc.

    context = {
        'audit_logs': audit_logs,
    }
    return render(request, 'itrc_tools/reports.html', context)
