from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from main.models import CustomUser, Status

@login_required
def insights_dashboard(request):
    """
    Displays a table of non‑counselor users with their latest status information.
    The table includes search filtering and pagination and uses hover effects and tooltips
    similar to the Contact dashboard.
    """
    search_query = request.GET.get('search', '')
    users = CustomUser.objects.filter(is_counselor=False)
    
    if search_query:
        users = users.filter(
            Q(full_name__icontains=search_query) | Q(username__icontains=search_query)
        )
    
    # Build a dictionary mapping each user's ID to their latest status.
    latest_status_map = {}
    for user in users:
        status = Status.objects.filter(user=user).order_by('-created_at').first()
        if status:
            latest_status_map[user.id] = status

    # Paginate the users (10 per page)
    paginator = Paginator(users.order_by('id'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'latest_status_map': latest_status_map,
    }
    return render(request, 'insights/dashboard.html', context)

@login_required
def user_analysis(request, user_id):
    """
    Detailed analysis view for a specific user.
    Displays the user's latest status in an elevated container with tooltip animations.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    latest_status = Status.objects.filter(user=user).order_by('-created_at').first()

    # Set threshold for critical emotions
    CRITICAL_THRESHOLD = 70
    critical = False
    concerning_emotions = []
    if latest_status:
        if latest_status.anger_percentage >= CRITICAL_THRESHOLD:
            concerning_emotions.append('Anger')
        if latest_status.sadness_percentage >= CRITICAL_THRESHOLD:
            concerning_emotions.append('Sadness')
        if latest_status.fear_percentage >= CRITICAL_THRESHOLD:
            concerning_emotions.append('Fear')
        if latest_status.disgust_percentage >= CRITICAL_THRESHOLD:
            concerning_emotions.append('Disgust')
        if concerning_emotions:
            critical = True

    context = {
        'user': user,
        'latest_status': latest_status,
        'critical': critical,
        'concerning_emotions': concerning_emotions,
    }
    return render(request, 'insights/user_analysis.html', context)
