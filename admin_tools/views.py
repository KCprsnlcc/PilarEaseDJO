# admin_tools/views.py

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q, Avg
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
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from main.models import Referral
from collections import Counter
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import timedelta
from datetime import datetime
import os
from django.conf import settings

# Ensure NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

@require_GET
def generate_wordcloud(request):
    text = request.GET.get('text', '')
    if not text:
        return HttpResponse('No text provided.', status=400)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format='PNG')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')   


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
def referral(request):
    if not request.user.is_counselor:
        return redirect('admin_login')
    referrals = Referral.objects.all().order_by('-created_at')
    profanities = Referral.objects.values_list('referral_reason', flat=True).distinct()
    return render(request, 'admin_tools/referral.html', {'referrals': referrals, 'profanities': profanities})

# ===========================
# Referral Management Views
# ===========================

@login_required
def get_referral_details(request, referral_id):
    """
    Fetch referral details for a given referral ID.
    """
    referral = get_object_or_404(Referral, id=referral_id)
    data = {
        'id': referral.id,
        'status': referral.status.title if referral.status else 'N/A',
        'title': referral.status.title if referral.status else '',
        'description': referral.status.description if referral.status else '',
        'referral_reason': referral.referral_reason,
        'other_reason': referral.other_reason,
    }
    return JsonResponse(data)

@login_required
@csrf_exempt
def add_profanity(request):
    """
    Add new words to the profanity list.
    Expects JSON data with a 'words' key containing a list of words.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            words = data.get('words', [])
            if not isinstance(words, list):
                return JsonResponse({'success': False, 'error': 'Invalid data format. "words" should be a list.'}, status=400)
            
            added_words = []
            for word in words:
                word = word.strip().lower()
                if word and not Referral.objects.filter(referral_reason__iexact=word).exists():
                    # Create a Referral entry with no associated status
                    Referral.objects.create(
                        status=None,
                        referred_by=request.user,
                        referral_reason=word,
                        created_at=timezone.now()
                    )
                    added_words.append(word)
            
            # Reload profanity filter
            profanity.load_censor_words()
    
            return JsonResponse({'success': True, 'added_words': added_words})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@login_required
@csrf_exempt
def delete_profanity(request):
    """
    Delete a word from the profanity list.
    Expects JSON data with a 'word' key.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            word = data.get('word', '').strip().lower()
            if not word:
                return JsonResponse({'success': False, 'error': 'No word provided.'}, status=400)
            
            # Delete all Referral entries where referral_reason matches the word
            deleted_count, _ = Referral.objects.filter(referral_reason__iexact=word).delete()
            if deleted_count > 0:
                # Reload profanity filter
                profanity.load_censor_words()
                return JsonResponse({'success': True, 'deleted_word': word})
            else:
                return JsonResponse({'success': False, 'error': 'Word not found in profanity list.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

def load_custom_profanities():
    """Load custom profanities from a text file in the main app's static directory."""
    # Define the path to the custom profanity file inside 'main/static/profanity/'
    profanity_file_path = os.path.join(settings.BASE_DIR, 'main', 'static', 'profanity', 'custom_profanities.txt')

    # Check if the file exists and load the custom profanities from the file
    if os.path.exists(profanity_file_path):
        with open(profanity_file_path, 'r', encoding='utf-8') as f:
            custom_profanities = [line.strip() for line in f.readlines()]
        return custom_profanities
    return []
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


@login_required
def manage_profanities(request):
    """
    View to manage the profanity list.
    Displays all profane words and provides options to add or delete.
    """
    profanities = Referral.objects.exclude(referral_reason='').values_list('referral_reason', flat=True).distinct()
    context = {
        'profanities': profanities,
    }
    return render(request, 'admin_tools/profanity_list.html', context)

def manage_referral(request):
    """
    View to manage referrals and the profanity list.
    """
    referrals = Referral.objects.all().order_by('-created_at')
    # Extract unique profane words from referral_reason
    profanities = Referral.objects.exclude(referral_reason='').values_list('referral_reason', flat=True).distinct()
    context = {
        'referrals': referrals,
        'profanities': profanities,
    }
    return render(request, 'admin_tools/referral.html', context)

@login_required
def referrals_api(request):
    """
    API endpoint to list all referrals. Useful for frontend JavaScript.
    """
    referrals = Referral.objects.all().values(
        'id',
        'status__title',
        'referred_by__username',
        'referral_reason',
        'other_reason',
        'created_at'
    )
    return JsonResponse(list(referrals), safe=False)


def chat(request):
    return render(request, 'admin_tools/chat.html')


@login_required
def statistics_view(request):
    # Retrieve filter parameters from GET request
    emotion_filter = request.GET.get('emotion', '')
    time_range = request.GET.get('time_range', '')
    text_search = request.GET.get('text_search', '')

    # Initial queryset
    statuses = Status.objects.all()

    # Apply Emotion Filter
    if emotion_filter:
        statuses = statuses.filter(emotion__iexact=emotion_filter)

    # Apply Time Range Filter
    if time_range:
        now = timezone.now()
        if time_range == 'last_week':
            start_date = now - timedelta(weeks=1)
        elif time_range == 'last_month':
            start_date = now - timedelta(days=30)
        elif time_range == 'last_year':
            start_date = now - timedelta(days=365)
        else:
            start_date = None

        if start_date:
            statuses = statuses.filter(created_at__gte=start_date)

    # Apply Text Search Filter
    if text_search:
        statuses = statuses.filter(
            Q(title__icontains=text_search) |
            Q(plain_description__icontains=text_search)
        )

    # Convert to values for DataFrame
    statuses = statuses.values()

    # Fetch all users
    users = CustomUser.objects.all().values()

    # Create DataFrames from the statuses and users
    df_statuses = pd.DataFrame(statuses)
    df_users = pd.DataFrame(users)

    # Fill NaN values with 0
    df_statuses.fillna(0, inplace=True)

    # Define emotion percentage columns
    emotion_percentage_columns = [
        'anger_percentage',
        'disgust_percentage',
        'fear_percentage',
        'neutral_percentage',
        'happiness_percentage',
        'sadness_percentage',
        'surprise_percentage'
    ]

    # Calculate emotion percentages
    if df_statuses.empty:
        emotion_percentages = [0 for _ in emotion_percentage_columns]
    else:
        emotion_percentages = df_statuses[emotion_percentage_columns].mean().round(2).tolist()

    # Data for Pie Chart (Emotion Percentages)
    pie_labels = [label.replace('_percentage', '').capitalize() for label in emotion_percentage_columns]
    pie_data = emotion_percentages

    # Data for Bar Chart (Emotion Distribution by Title)
    if 'title' in df_statuses.columns:
        df_melted = df_statuses.melt(id_vars=['title'], value_vars=emotion_percentage_columns, var_name='emotion', value_name='percentage')
        df_melted['emotion'] = df_melted['emotion'].str.replace('_percentage', '').str.capitalize()
        bar_chart_data = df_melted.groupby(['title', 'emotion'])['percentage'].mean().unstack().fillna(0).round(2)
        bar_labels = bar_chart_data.index.tolist()
        bar_datasets = []
        colors = {
            'Anger': '#f44336',
            'Disgust': '#9c27b0',
            'Fear': '#3f51b5',
            'Happiness': '#ffeb3b',
            'Sadness': '#2196f3',
            'Surprise': '#ff9800',
            'Neutral': '#9e9e9e',
        }

        for emotion in pie_labels:
            if emotion in bar_chart_data.columns:
                bar_datasets.append({
                    'label': emotion,
                    'backgroundColor': colors.get(emotion, '#000000'),
                    'data': bar_chart_data[emotion].tolist(),
                })
    else:
        bar_labels = []
        bar_datasets = []

    # Word Cloud Data (handled in template via image)
    if 'plain_description' in df_statuses.columns and not df_statuses['plain_description'].isnull().all():
        text = " ".join(df_statuses['plain_description'].astype(str).tolist())
    else:
        text = ""

    # Calculate total students
    total_students = df_users['id'].nunique()

    # Calculate positive, neutral, negative percentages
    if df_statuses.empty:
        positive_percent = 0
        neutral_percent = 0
        negative_percent = 0
    else:
        positive_percent = df_statuses['happiness_percentage'].mean()
        neutral_percent = df_statuses['neutral_percentage'].mean()
        negative_percent = (
            df_statuses['anger_percentage'].mean() +
            df_statuses['fear_percentage'].mean() +
            df_statuses['sadness_percentage'].mean()
        )

    # New: Emotion Trend Over Time (Line Chart)
    if 'created_at' in df_statuses.columns and not df_statuses['created_at'].isnull().all():
        df_statuses['created_at'] = pd.to_datetime(df_statuses['created_at'])
        df_statuses['month_year'] = df_statuses['created_at'].dt.to_period('M').astype(str)
        sentiment_columns_line = [
            'happiness_percentage',
            'neutral_percentage',
            'anger_percentage',
            'fear_percentage',
            'sadness_percentage'
        ]
        sentiment_trends = df_statuses.groupby('month_year')[sentiment_columns_line].mean().reset_index()

        line_labels = sentiment_trends['month_year'].tolist()
        line_datasets = []
        line_colors = {
            'happiness_percentage': '#4caf50',
            'neutral_percentage': '#ff9800',
            'anger_percentage': '#f44336',
            'fear_percentage': '#9c27b0',
            'sadness_percentage': '#2196f3',
        }

        for sentiment in sentiment_columns_line:
            capital_emotion = sentiment.replace('_percentage', '').capitalize()
            line_datasets.append({
                'label': capital_emotion,
                'borderColor': line_colors.get(sentiment, '#000000'),
                'fill': False,
                'data': sentiment_trends[sentiment].round(2).tolist(),
            })
    else:
        line_labels = []
        line_datasets = []

    # New: Emotion Frequency (Bar Chart)
    frequency_labels = [label.replace('_percentage', '').capitalize() for label in emotion_percentage_columns]
    if not df_statuses.empty:
        frequency_data = df_statuses[emotion_percentage_columns].count().tolist()
    else:
        frequency_data = [0 for _ in emotion_percentage_columns]

    # New: Emotion Intensity Gauge (Donut Chart)
    intensity_labels = ['Happiness', 'Neutral', 'Anger', 'Fear', 'Sadness']
    if not df_statuses.empty:
        intensity_data = [
            int(df_statuses['happiness_percentage'].mean()),
            int(df_statuses['neutral_percentage'].mean()),
            int(df_statuses['anger_percentage'].mean()),
            int(df_statuses['fear_percentage'].mean()),
            int(df_statuses['sadness_percentage'].mean()),
        ]
    else:
        intensity_data = [0, 0, 0, 0, 0]

    # New: Emotion Pulse (Area Chart)
    if not df_statuses.empty and not sentiment_trends.empty:
        pulse_labels = sentiment_trends['month_year'].tolist()
        pulse_datasets = []
        pulse_colors = {
            'Happiness': 'rgba(76, 175, 80, 0.5)',
            'Neutral': 'rgba(255, 152, 0, 0.5)',
            'Anger': 'rgba(244, 67, 54, 0.5)',
            'Fear': 'rgba(156, 39, 176, 0.5)',
            'Sadness': 'rgba(33, 150, 243, 0.5)',
        }

        for sentiment in ['Happiness', 'Neutral', 'Anger', 'Fear', 'Sadness']:
            pulse_datasets.append({
                'label': sentiment,
                'backgroundColor': pulse_colors.get(sentiment, 'rgba(0,0,0,0.5)'),
                'borderColor': line_colors.get(sentiment.lower() + '_percentage', '#000000'),
                'fill': True,
                'data': sentiment_trends[f'{sentiment.lower()}_percentage'].round(2).tolist(),
            })
    else:
        pulse_labels = []
        pulse_datasets = []

    # Context Variables
    context = {
        'pie_labels': json.dumps(pie_labels),
        'pie_data': json.dumps(pie_data),
        'bar_labels': json.dumps(bar_labels),
        'bar_datasets': json.dumps(bar_datasets),
        'wordcloud_text': text,
        'total_students': total_students,
        'positive_percent': int(round(positive_percent, 0)),
        'neutral_percent': int(round(neutral_percent, 0)),
        'negative_percent': int(round(negative_percent, 0)),
        # New Chart Data
        'line_labels': json.dumps(line_labels),
        'line_datasets': json.dumps(line_datasets),
        'frequency_labels': json.dumps(frequency_labels),
        'frequency_data': json.dumps(frequency_data),
        'intensity_labels': json.dumps(intensity_labels),
        'intensity_data': json.dumps(intensity_data),
        'pulse_labels': json.dumps(pulse_labels),
        'pulse_datasets': json.dumps(pulse_datasets),
    }
    return render(request, 'admin_tools/statistics.html', context)

# admin_tools/views.py

@login_required
def sentiment_analytics_view(request):
    # Fetch all statuses
    statuses = Status.objects.all().values()
    df_statuses = pd.DataFrame(statuses)
    df_statuses.fillna(0, inplace=True)

    # Convert created_at to datetime
    df_statuses['created_at'] = pd.to_datetime(df_statuses['created_at'])

    # Extract month and year
    df_statuses['month_year'] = df_statuses['created_at'].dt.to_period('M').astype(str)

    # Calculate average sentiment scores per month
    sentiment_columns = ['happiness', 'neutral', 'anger', 'fear', 'sadness']
    sentiment_trends = df_statuses.groupby('month_year')[sentiment_columns].mean().reset_index()

    # Prepare data for Line Chart
    line_labels = sentiment_trends['month_year'].tolist()
    line_datasets = []
    colors = {
        'happiness': '#4caf50',
        'neutral': '#ff9800',
        'anger': '#f44336',
        'fear': '#9c27b0',
        'sadness': '#2196f3',
    }

    for sentiment in sentiment_columns:
        line_datasets.append({
            'label': sentiment.capitalize(),
            'borderColor': colors.get(sentiment, '#000000'),
            'fill': False,
            'data': sentiment_trends[sentiment].round(2).tolist(),
        })

    context = {
        'line_labels': json.dumps(line_labels),
        'line_datasets': json.dumps(line_datasets),
    }
    return render(request, 'admin_tools/sentiment_analytics.html', context)

# Mock Profanity Filter (Replace with actual implementation)
class ProfanityFilter:
    def __init__(self):
        self.profanities = set()
    
    def load_censor_words(self):
        # Load custom profanities from Referral's referral_reason
        self.profanities = set(
            Referral.objects.exclude(referral_reason='').values_list('referral_reason', flat=True)
        )
    
    def contains_profanity(self, text):
        tokens = word_tokenize(text.lower())
        return any(word in self.profanities for word in tokens)

profanity = ProfanityFilter()
profanity.load_censor_words()

def load_custom_profanities():
    """Load custom profanities from the Referral model."""
    return Referral.objects.exclude(referral_reason='').values_list('referral_reason', flat=True)

def contains_custom_profanity(text):
    """Check if the text contains any custom profanities."""
    custom_profanities = load_custom_profanities()
    for profanity_word in custom_profanities:
        if re.search(rf'\b{re.escape(profanity_word)}\b', text, re.IGNORECASE):
            return True
    return False

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

    # --- Contextual Emotion Comparison User Table ---
    # Calculate average emotion percentages for each user based on their recent statuses
    recent_statuses = Status.objects.filter(created_at__gte=timezone.now() - timedelta(days=30))
    user_emotions = recent_statuses.values('user__id', 'user__full_name').annotate(
        avg_anger=Avg('anger_percentage'),
        avg_disgust=Avg('disgust_percentage'),
        avg_fear=Avg('fear_percentage'),
        avg_neutral=Avg('neutral_percentage'),
        avg_happiness=Avg('happiness_percentage'),
        avg_sadness=Avg('sadness_percentage'),
        avg_surprise=Avg('surprise_percentage'),
    )

    # Prepare comparison data: current status vs average
    comparison_data = []
    for status in page_obj:
        user = status.user
        averages = user_emotions.filter(user__id=user.id).order_by('user__id').first()
        if averages:
            comparison = {
                'user_full_name': user.full_name,
                'current_status': {
                    'anger': status.anger_percentage,
                    'disgust': status.disgust_percentage,
                    'fear': status.fear_percentage,
                    'neutral': status.neutral_percentage,
                    'happiness': status.happiness_percentage,
                    'sadness': status.sadness_percentage,
                    'surprise': status.surprise_percentage,
                },
                'average_recent': {
                    'anger': round(averages['avg_anger'], 2) if averages['avg_anger'] else 0,
                    'disgust': round(averages['avg_disgust'], 2) if averages['avg_disgust'] else 0,
                    'fear': round(averages['avg_fear'], 2) if averages['avg_fear'] else 0,
                    'neutral': round(averages['avg_neutral'], 2) if averages['avg_neutral'] else 0,
                    'happiness': round(averages['avg_happiness'], 2) if averages['avg_happiness'] else 0,
                    'sadness': round(averages['avg_sadness'], 2) if averages['avg_sadness'] else 0,
                    'surprise': round(averages['avg_surprise'], 2) if averages['avg_surprise'] else 0,
                }
            }
            comparison_data.append(comparison)

    # --- Keywords or Topics Detection ---
    # Function to extract keywords from text
    def extract_keywords(text, num_keywords=5):
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        word_counts = Counter(filtered_tokens)
        common_words = [word for word, count in word_counts.most_common(num_keywords)]
        return common_words

    # Extract keywords for each status
    keywords_data = []
    for status in page_obj:
        keywords = extract_keywords(status.plain_description)
        keywords_data.append({
            'status_id': status.id,
            'keywords': keywords
        })

    context = {
        'statuses': page_obj,
        'search_query': search_query,
        'category': category,
        'page_obj': page_obj,
        'comparison_data': comparison_data,
        'keywords_data': keywords_data,
    }
    return render(request, 'admin_tools/analysis.html', context)

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
