# admin_tools/views.py

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from main.models import ContactUs, Status, CustomUser, Reply
import pandas as pd
import plotly.express as px
import plotly.io as pio
from wordcloud import WordCloud
from io import BytesIO
import base64


@login_required
def replies_view(request):
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)
    
    replies = Reply.objects.select_related('status', 'user').all()
    
    if search_query:
        replies = replies.filter(
            Q(user__username__icontains=search_query) |
            Q(status__title__icontains=search_query) |
            Q(text__icontains=search_query)
        )
    
    paginator = Paginator(replies, 10)  # 10 replies per page
    page_obj = paginator.get_page(page_number)

    context = {
        'replies': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query
    }

    return render(request, 'admin_tools/replies.html', context)

@login_required
def delete_reply(request, reply_id):
    if request.method == 'DELETE':
        try:
            reply = Reply.objects.get(id=reply_id)
            reply.delete()
            return JsonResponse({'success': True, 'message': 'Reply deleted successfully.'})
        except Reply.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reply not found.'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

@login_required
def status_view(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', 'all')
    page_number = request.GET.get('page', 1)
    page_size = 10

    # Filter statuses based on search query and category
    if category == 'all':
        statuses = Status.objects.filter(
            Q(title__icontains=search_query) |
            Q(plain_description__icontains=search_query)
        )
    else:
        statuses = Status.objects.filter(
            Q(title__icontains=search_query) |
            Q(plain_description__icontains=search_query),
            emotion=category
        )

    paginator = Paginator(statuses, page_size)
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_tools/status.html', {
        'statuses': page_obj,
        'search_query': search_query,
        'category': category,
        'page_obj': page_obj,
    })

def generate_base64_image(fig):
    img_bytes = pio.to_image(fig, format="png", engine="kaleido")
    return base64.b64encode(img_bytes).decode('utf-8')

@login_required
def statistics_view(request):
    # Fetch all statuses
    statuses = Status.objects.all().values()
    # Fetch all users
    users = CustomUser.objects.all().values()

    # Create DataFrames from the statuses and users
    df_statuses = pd.DataFrame(statuses)
    df_users = pd.DataFrame(users)

    # Fill NaN values with 0
    df_statuses.fillna(0, inplace=True)

    # Calculate emotion percentages
    emotion_columns = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise', 'neutral']
    emotion_percentages = df_statuses[emotion_columns].mean() * 100

    # Generate pie chart for emotions using Plotly
    fig_pie = px.pie(values=emotion_percentages, names=emotion_columns, title='Emotion Percentages')
    emotion_chart_image_base64 = generate_base64_image(fig_pie)

    # Generate word cloud for plain descriptions
    text = " ".join(df_statuses['plain_description'].fillna(''))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format='png')
    buffer.seek(0)
    wordcloud_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Generate bar chart for title-based emotions using Plotly
    df_melted = df_statuses.melt(id_vars=['title'], value_vars=emotion_columns)
    fig_bar = px.bar(df_melted, x='title', y='value', color='variable', title='Emotion Distribution by Title')
    bar_chart_image_base64 = generate_base64_image(fig_bar)

    # Calculate total students
    total_students = df_users['id'].nunique()

    # Calculate positive, neutral, negative percentages
    positive_percent = df_statuses['happiness'].fillna(0).mean() * 100
    neutral_percent = df_statuses[['surprise', 'disgust']].fillna(0).mean().mean() * 100
    negative_percent = df_statuses[['anger', 'fear', 'sadness']].fillna(0).mean().mean() * 100

    return render(request, 'admin_tools/statistics.html', {
        'emotion_chart_image_base64': emotion_chart_image_base64,
        'wordcloud_image_base64': wordcloud_image_base64,
        'bar_chart_image_base64': bar_chart_image_base64,
        'positive_percent': positive_percent,
        'neutral_percent': neutral_percent,
        'negative_percent': negative_percent,
        'total_students': total_students
    })

@login_required
def analysis_view(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', 'all')
    page_number = request.GET.get('page', 1)
    page_size = 10

    # Filter statuses based on search query and category
    if category == 'all':
        statuses = Status.objects.filter(
            Q(title__icontains=search_query) |
            Q(plain_description__icontains=search_query)
        )
    else:
        statuses = Status.objects.filter(
            Q(title__icontains=search_query) |
            Q(plain_description__icontains=search_query),
            emotion=category
        )

    paginator = Paginator(statuses, page_size)
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_tools/analysis.html', {
        'statuses': page_obj,
        'search_query': search_query,
        'category': category,
        'page_obj': page_obj,
    })

@login_required
def contact_us_view(request):
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)
    page_size = 10

    # Filter contact us queries based on search query
    contacts = ContactUs.objects.filter(
        Q(name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(subject__icontains=search_query) |
        Q(message__icontains=search_query)
    )

    paginator = Paginator(contacts, page_size)
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_tools/dashboard.html', {
        'contacts': page_obj,
        'search_query': search_query,
        'page_obj': page_obj,
    })

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
def reports(request):
    if not request.user.is_counselor:
        return redirect('login')
    return render(request, 'admin_tools/reports.html')



@login_required
def manage_users_view(request):
    search_query = request.GET.get('search', '')
    users = CustomUser.objects.all()

    if search_query:
        users = users.filter(username__icontains=search_query)

    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'manage_users.html', context)

@login_required
def settings(request):
    if not request.user.is_counselor:
        return redirect('login')
    return render(request, 'admin_tools/settings.html')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
