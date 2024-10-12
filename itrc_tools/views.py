# itrc_tools/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from main.models import CustomUser
from .models import VerificationRequest, EnrollmentMasterlist, SystemSetting, AuditLog
from .forms import UploadMasterlistForm, SystemSettingForm
import csv
import io
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone

def is_itrc_staff(user):
    return user.is_authenticated and user.is_itrc_staff

@user_passes_test(is_itrc_staff)
@login_required
def itrc_dashboard(request):
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
    user = get_object_or_404(CustomUser, id=user_id)
    verification_request = get_object_or_404(VerificationRequest, user=user)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '')

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

        return redirect('itrc_dashboard')

    context = {
        'user_obj': user,
        'verification_request': verification_request,
    }
    return render(request, 'itrc_tools/verify_user.html', context)

@user_passes_test(is_itrc_staff)
@login_required
def upload_masterlist(request):
    if request.method == 'POST':
        form = UploadMasterlistForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a valid CSV file.')
                return redirect('upload_masterlist')

            try:
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                reader = csv.DictReader(io_string)
                with transaction.atomic():
                    for row in reader:
                        EnrollmentMasterlist.objects.update_or_create(
                            student_id=row['student_id'],
                            defaults={
                                'full_name': row['full_name'],
                                'academic_year_level': row['academic_year_level'],
                                'contact_number': row.get('contact_number', ''),
                                'email': row.get('email', ''),
                            }
                        )
                messages.success(request, 'Enrollment masterlist has been successfully uploaded and updated.')
                # Log the action
                AuditLog.objects.create(
                    user=request.user,
                    action='upload_masterlist',
                    details=f"Uploaded masterlist with {reader.line_num - 1} records."
                )
                return redirect('itrc_dashboard')
            except Exception as e:
                messages.error(request, f'An error occurred while processing the file: {e}')
                return redirect('upload_masterlist')
    else:
        form = UploadMasterlistForm()
    return render(request, 'itrc_tools/upload_masterlist.html', {'form': form})

@user_passes_test(is_itrc_staff)
@login_required
def manage_users(request):
    search_query = request.GET.get('search', '')
    if search_query:
        users = CustomUser.objects.filter(
            models.Q(username__icontains=search_query) |
            models.Q(student_id__icontains=search_query) |
            models.Q(full_name__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )
    else:
        users = CustomUser.objects.all()

    # Exclude ITRC staff and counselors from being managed here if necessary
    users = users.exclude(is_itrc_staff=True, is_counselor=True)

    # Pagination (optional)
    from django.core.paginator import Paginator
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'search_query': search_query,
    }
    return render(request, 'itrc_tools/manage_users.html', context)

# itrc_tools/views.py

from django.views.decorators.http import require_POST
from django.http import JsonResponse

@user_passes_test(is_itrc_staff)
@login_required
@require_POST
def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
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
    user = get_object_or_404(CustomUser, id=user_id)
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
    user = get_object_or_404(CustomUser, id=user_id)
    username = user.username
    user.delete()

    # Log the action
    AuditLog.objects.create(
        user=request.user,
        action='delete_user',
        details=f"Deleted user {username}."
    )

    return JsonResponse({'success': True, 'message': f'User {username} has been deleted.'})

# itrc_tools/views.py

@user_passes_test(is_itrc_staff)
@login_required
def system_settings(request):
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
            else:
                messages.success(request, f'System setting "{key}" has been updated.')
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='update_setting',
                details=f"Updated setting {key} to {value}."
            )
            return redirect('system_settings')
    else:
        form = SystemSettingForm()
    context = {
        'settings': settings_qs,
        'form': form,
    }
    return render(request, 'itrc_tools/system_settings.html', context)

# itrc_tools/views.py

@user_passes_test(is_itrc_staff)
@login_required
def generate_reports(request):
    audit_logs = AuditLog.objects.all().order_by('-timestamp')

    # Implement filtering based on GET parameters if needed
    # For example, filter by user, action, date range, etc.

    context = {
        'audit_logs': audit_logs,
    }
    return render(request, 'itrc_tools/reports.html', context)
