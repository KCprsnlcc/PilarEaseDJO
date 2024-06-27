from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime
import pytz
import json
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.hashers import check_password

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

@login_required
def get_user_profile(request):
    user_profile = CustomUser.objects.get(id=request.user.id)
    data = {
        'student_id': user_profile.student_id,
        'username': user_profile.username,
        'full_name': user_profile.full_name,
        'academic_year_level': user_profile.academic_year_level,
        'contact_number': user_profile.contact_number,
        'email': user_profile.email,
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

        # Check the current password before updating the new password
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
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'Logout successful!', 'redirect_url': '/'})
    return redirect('home')
