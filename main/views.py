from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
from .forms import CustomUserCreationForm, CustomAuthenticationForm

CustomUser = get_user_model()  # Get the custom user model

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
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/'})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({'success': False, 'error_message': errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'base.html', {'register_form': form, 'show_register_modal': False})

def login_view(request):
    if request.method == 'POST':
        print(f"CSRF token received: {request.META.get('CSRF_COOKIE')}")  # Debug log for CSRF token
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Attempting to authenticate user: {username}")  # Debug log
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("Authentication successful")  # Debug log
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/'})
            else:
                print("Authentication failed: invalid credentials")  # Debug log
                form.add_error(None, "Invalid login credentials")
        else:
            print("Form validation failed")  # Debug log
        errors = form.errors.get_json_data()
        print(f"Errors: {errors}")  # Debug log
        return JsonResponse({'success': False, 'error_message': errors})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'base.html', {'login_form': form, 'show_login_modal': True})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'Logout successful!', 'redirect_url': '/'})
    return redirect('home')
