from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils import timezone
from datetime import datetime
import pytz
import json
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AvatarUploadForm
from django.contrib.auth.hashers import check_password
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import UserProfile
import logging
from PIL import Image
from io import BytesIO
import os
from .models import Status
import re
from django.utils.timesince import timesince
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)
CustomUser = get_user_model()

def current_time_view(request):
    tz = pytz.timezone('Asia/Manila')
    current_time = datetime.now(tz)
    return HttpResponse(f"The current time in Manila is: {current_time}")

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'redirect_url': '/login/'})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({'success': False, 'error_message': errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'base.html', {'register_form': form, 'show_register_modal': False})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/'})
            else:
                form.add_error(None, "Invalid login credentials")
        errors = form.errors.get_json_data()
        return JsonResponse({'success': False, 'error_message': errors})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'base.html', {'login_form': form, 'show_login_modal': True})

def strip_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

@login_required
@csrf_exempt
def submit_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        emotion = data.get('emotion')
        title = data.get('title')
        description = data.get('description')
        plain_description = strip_html_tags(description)
        
        # Validate the input fields
        errors = {}
        if not emotion:
            errors['emotion'] = 'This field is required.'
        if not title:
            errors['title'] = 'This field is required.'
        if not description:
            errors['description'] = 'This field is required.'

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Save the status to the database
        status = Status.objects.create(
            user=request.user,
            emotion=emotion,
            title=title,
            description=description,
            plain_description=plain_description
        )

        # Prepare the status data to return
        status_data = {
            'id': status.id,
            'username': request.user.username,
            'avatar_url': request.user.profile.avatar.url if request.user.profile.avatar else None,
            'emotion': status.emotion,
            'title': status.title,
            'description': status.plain_description,
            'created_at': timesince(status.created_at),
            'replies': 0  # Placeholder for replies
        }

        return JsonResponse({'success': True, 'status': status_data, 'message': 'Status shared successfully!'})

    return JsonResponse({'success': False, 'errors': {'non_field_errors': 'Invalid request method'}}, status=400)

def get_all_statuses(request):
    page_number = request.GET.get('page', 1)
    page_size = 10  # Number of statuses per page
    category = request.GET.get('category', 'recent')

    if category == 'recent':
        statuses = Status.objects.all().order_by('-created_at')
    elif category == 'popular':
        statuses = Status.objects.annotate(reply_count=Count('replies')).order_by('-reply_count', '-created_at')
    else:
        statuses = Status.objects.filter(emotion__iexact=category).order_by('-created_at')

    paginator = Paginator(statuses, page_size)
    page_obj = paginator.get_page(page_number)

    authenticated_user_id = request.user.id if request.user.is_authenticated else None

    default_avatar_url = "/static/images/avatars/placeholder.png"

    statuses_data = [
        {
            'id': status.id,
            'username': status.user.username,
            'avatar_url': status.user.profile.avatar.url if status.user.profile.avatar else default_avatar_url,
            'emotion': status.emotion,
            'title': status.title,
            'description': status.plain_description,
            'created_at': timesince(status.created_at).split(',')[0],  # Take only the first part
            'replies': 0,  # Placeholder for replies
            'can_delete': status.user.id == authenticated_user_id
        }
        for status in page_obj
    ]
    return JsonResponse({'statuses': statuses_data, 'has_next': page_obj.has_next()})


@login_required
@csrf_exempt
def delete_status(request, status_id):
    if request.method == 'DELETE':
        try:
            status = Status.objects.get(id=status_id, user=request.user)
            status.delete()
            return JsonResponse({'success': True, 'message': 'Status deleted successfully.'})
        except Status.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Status not found or you do not have permission to delete this status.'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

@login_required
def get_user_profile(request):
    user_profile = request.user.profile
    default_avatar_url = "/static/images/avatars/placeholder.png"
    avatar_url = user_profile.avatar.url if user_profile.avatar else default_avatar_url
    data = {
        'student_id': request.user.student_id,
        'username': request.user.username,
        'full_name': request.user.full_name,
        'academic_year_level': request.user.academic_year_level,
        'contact_number': request.user.contact_number,
        'email': request.user.email,
        'avatar': avatar_url,
    }
    return JsonResponse(data)

@login_required
@csrf_exempt
def update_user_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        contact_number = data.get('contact_number')
        email = data.get('email')
        academic_year_level = data.get('academic_year_level')
        user = request.user
        response_data = {'success': True, 'errors': {}}

        # Check if the username or email already exists for another user
        if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
            response_data['success'] = False
            response_data['errors']['username'] = 'Username already exists.'

        if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
            response_data['success'] = False
            response_data['errors']['email'] = 'Email already registered by another user.'
            
        # Update the user details if there are no errors
        if response_data['success']:
            user.username = username
            user.contact_number = contact_number
            user.email = email
            user.academic_year_level = academic_year_level
            user.save()
        else:
            return JsonResponse(response_data, status=400)
        return JsonResponse({'success': True, 'message': 'Profile updated successfully!'})

    return JsonResponse({'success': False, 'errors': {'non_field_errors': 'Invalid request'}}, status=400)

@login_required
@csrf_exempt
def password_manager_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        repeat_new_password = data.get('repeat_new_password')

        user = request.user
        response_data = {'success': True, 'errors': {}}

        if not check_password(current_password, user.password):
            response_data['success'] = False
            response_data['errors']['current_password'] = 'Please check your current password.'
        elif new_password != repeat_new_password:
            response_data['success'] = False
            response_data['errors']['new_password'] = 'Passwords do not match.'
        else:
            user.set_password(new_password)
            user.save()

        if response_data['success']:
            return JsonResponse({'success': True, 'message': 'Password updated successfully!'})
        else:
            return JsonResponse(response_data, status=400)

    return JsonResponse({'success': False, 'errors': {'non_field_errors': 'Invalid request'}}, status=400)

@login_required
@csrf_exempt
def upload_avatar(request):
    if request.method == 'POST':
        user_profile = request.user.profile

        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']

            # Check file size (limit to 1MB)
            if avatar.size > 1 * 1024 * 1024:
                return JsonResponse({'success': False, 'errors': 'File size exceeds the 1MB limit.'}, status=400)

            # Save the image file directly
            user_profile.avatar.save(avatar.name, avatar)
            user_profile.save()

            return JsonResponse({'success': True, 'avatar_url': user_profile.avatar.url})

        return JsonResponse({'success': False, 'errors': 'No avatar file uploaded.'}, status=400)

    return JsonResponse({'success': False, 'errors': 'Invalid request'}, status=400)

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'Logout successful!', 'redirect_url': '/'})
    return redirect('home')