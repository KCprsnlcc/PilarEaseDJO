# admin_tools/views.py

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_counselor:
        return HttpResponseRedirect(reverse('admin_dashboard'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_counselor:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_tools/admin_login.html', {'error': 'Invalid credentials or not authorized.'})
    
    return render(request, 'admin_tools/admin_login.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_counselor:
        return redirect('login')
    return render(request, 'admin_tools/dashboard.html')

@login_required
def statistics(request):
    if not request.user.is_counselor:
        return redirect('login')
    return render(request, 'admin_tools/statistics.html')

@login_required
def analysis(request):
    if not request.user.is_counselor:
        return redirect('login')
    return render(request, 'admin_tools/analysis.html')

@login_required
def reports(request):
    if not request.user.is_counselor:
        return redirect('login')
    return render(request, 'admin_tools/reports.html')


@login_required
def status(request):
    if not request.user.is_counselor:
        return redirect('login')
    return render(request, 'admin_tools/status.html')

@login_required
def replies(request):
    if not request.user.is_counselor:
        return redirect('login')
    return render(request, 'admin_tools/replies.html')

@login_required
def manage_users(request):
    if not request.user.is_counselor:
        return redirect('login')
    return render(request, 'admin_tools/manage_users.html')

@login_required
def settings(request):
    if not request.user.is_counselor:
        return redirect('login')
    return render(request, 'admin_tools/settings.html')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
