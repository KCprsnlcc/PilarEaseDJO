# admin_tools/views.py

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from main.models import (
    ContactUs,
    Status,
    CustomUser,
    Reply,
    Feedback,
)
import pandas as pd
import plotly.express as px
import plotly.io as pio
from wordcloud import WordCloud
from io import BytesIO
import base64
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timesince import timesince
from datetime import datetime
from django.utils import timezone

def generate_base64_image(fig):
    img_bytes = pio.to_image(fig, format="png", engine="kaleido")
    return base64.b64encode(img_bytes).decode('utf-8')


@login_required
def replies_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        replies = Reply.objects.filter(text__icontains=search_query)
    else:
        replies = Reply.objects.all()

    paginator = Paginator(replies, 10)  # Show 10 replies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_time = timezone.now()

    replies_data = [
        {
            'id': reply.id,
            'student_id': reply.user.student_id,
            'username': reply.user.username,
            'status_title': reply.status.title,
            'text': reply.text,
            'created_at': reply.created_at,
            'last_sent': timesince(reply.created_at, current_time)
        }
        for reply in page_obj
    ]

    context = {
        'replies': replies_data,
        'search_query': search_query,
        'page_obj': page_obj,
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


@login_required
def dashboard(request):
    # Feedbacks
    feedback_search_query = request.GET.get('feedback_search', '')
    feedbacks_queryset = Feedback.objects.all()
    if feedback_search_query:
        feedbacks_queryset = feedbacks_queryset.filter(
            Q(user__full_name__icontains=feedback_search_query) |
            Q(message__icontains=feedback_search_query)
        )
    feedbacks_paginator = Paginator(feedbacks_queryset, 10)  # Show 10 feedbacks per page
    feedback_page_number = request.GET.get('page_feedback')
    feedbacks = feedbacks_paginator.get_page(feedback_page_number)

    # Testimonials (approved feedbacks)
    testimonial_search_query = request.GET.get('testimonial_search', '')
    testimonials_queryset = Feedback.objects.filter(is_approved=True)
    if testimonial_search_query:
        testimonials_queryset = testimonials_queryset.filter(
            Q(user__full_name__icontains=testimonial_search_query) |
            Q(message__icontains=testimonial_search_query)
        )
    testimonials_paginator = Paginator(testimonials_queryset, 10)  # Show 10 testimonials per page
    testimonial_page_number = request.GET.get('page_testimonial')
    testimonials = testimonials_paginator.get_page(testimonial_page_number)

    # Contact Us Queries
    contact_search_query = request.GET.get('contact_search', '')
    contacts_queryset = ContactUs.objects.all()
    if contact_search_query:
        contacts_queryset = contacts_queryset.filter(
            Q(name__icontains=contact_search_query) |
            Q(email__icontains=contact_search_query) |
            Q(subject__icontains=contact_search_query) |
            Q(message__icontains=contact_search_query)
        )
    contacts_paginator = Paginator(contacts_queryset, 10)  # Show 10 contacts per page
    contact_page_number = request.GET.get('page_contact')
    contacts = contacts_paginator.get_page(contact_page_number)

    context = {
        'feedbacks': feedbacks,
        'feedback_search_query': feedback_search_query,
        'testimonials': testimonials,
        'testimonial_search_query': testimonial_search_query,
        'contacts': contacts,
        'contact_search_query': contact_search_query,
    }
    return render(request, 'admin_tools/dashboard.html', context)


@login_required
def approve_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.is_approved = True
    feedback.save()
    return redirect('dashboard')


@login_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    return redirect('dashboard')


@login_required
def approve_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Feedback, id=testimonial_id)
    testimonial.is_approved = True
    testimonial.save()
    return redirect('dashboard')


@login_required
def delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Feedback, id=testimonial_id)
    testimonial.delete()
    return redirect('dashboard')


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

    if request.method == 'POST':
        # Handle reply to contact query
        contact_id = request.POST.get('contact_id')
        reply_text = request.POST.get('reply_text')
        if contact_id and reply_text:
            try:
                contact = ContactUs.objects.get(id=contact_id)
                # Assuming ContactUs has a 'reply' field or related model
                # For simplicity, we'll add a 'reply' field in ContactUs
                contact.reply = reply_text
                contact.is_replied = True
                contact.save()
                # Optionally, send an email to the user
                # send_mail(
                #     'Re: ' + contact.subject,
                #     reply_text,
                #     'admin@pilarease.com',
                #     [contact.email],
                #     fail_silently=False,
                # )
                return redirect('dashboard')
            except ContactUs.DoesNotExist:
                pass

    context = {
        'contacts': page_obj,
        'search_query': search_query,
        'page_obj': page_obj,
    }
    return render(request, 'admin_tools/dashboard.html', context)


def home(request):
    return render(request, 'home.html')


def manage_referral(request):
    referrals = Referral.objects.all()
    context = {
        'referrals': referrals,
    }
    return render(request, 'admin_tools/manage_referral.html', context)


def chat(request):
    return render(request, 'admin_tools/chat.html')


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

    if request.method == 'POST':
        # Handle reply to contact query
        contact_id = request.POST.get('contact_id')
        reply_text = request.POST.get('reply_text')
        if contact_id and reply_text:
            try:
                contact = ContactUs.objects.get(id=contact_id)
                # Assuming ContactUs has a 'reply' field or related model
                # For simplicity, we'll add a 'reply' field in ContactUs
                contact.reply = reply_text
                contact.is_replied = True
                contact.save()
                # Optionally, send an email to the user
                # send_mail(
                #     'Re: ' + contact.subject,
                #     reply_text,
                #     'admin@pilarease.com',
                #     [contact.email],
                #     fail_silently=False,
                # )
                return redirect('dashboard')
            except ContactUs.DoesNotExist:
                pass

    context = {
        'contacts': page_obj,
        'search_query': search_query,
        'page_obj': page_obj,
    }
    return render(request, 'admin_tools/dashboard.html', context)


def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_counselor:
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_counselor:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'admin_tools/admin_login.html', {'error': 'Invalid credentials or not authorized.'})
    
    return render(request, 'admin_tools/admin_login.html')


@login_required
def reports(request):
    if not request.user.is_counselor:
        return redirect('admin_login')
    return render(request, 'admin_tools/reports.html')


@login_required
def manage_users_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        users = CustomUser.objects.filter(username__icontains=search_query)
    else:
        users = CustomUser.objects.all()

    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'search_query': search_query,
        'page_obj': page_obj,
    }
    return render(request, 'admin_tools/manage_users.html', context)


@login_required
@csrf_exempt
def block_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        reason = data.get('reason')
        duration = data.get('duration')

        try:
            user = CustomUser.objects.get(id=user_id)
            user.is_active = False
            user.block_reason = reason
            user.block_duration = duration
            user.save()
            return JsonResponse({'success': True})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def contact_us_reply(request, contact_id):
    if request.method == 'POST':
        reply_text = request.POST.get('reply_text')
        if reply_text:
            try:
                contact = ContactUs.objects.get(id=contact_id)
                contact.reply = reply_text
                contact.is_replied = True
                contact.save()
                # Optionally, send an email to the user
                from django.core.mail import send_mail
                send_mail(
                    f"Re: {contact.subject}",
                    reply_text,
                    'admin@pilarease.com',
                    [contact.email],
                    fail_silently=False,
                )
                return redirect('dashboard')
            except ContactUs.DoesNotExist:
                pass
    return redirect('dashboard')


@login_required
def delete_contact_us(request, contact_id):
    contact = get_object_or_404(ContactUs, id=contact_id)
    contact.delete()
    return redirect('dashboard')

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('manage_users')


@login_required
def settings(request):
    if not request.user.is_counselor:
        return redirect('admin_login')
    return render(request, 'admin_tools/settings.html')


@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
