from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
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
from .models import Status, Reply, ContactUs, Referral, ChatMessage, Questionnaire
import re
from django.utils.timesince import timesince
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from wordcloud import WordCloud
from django.shortcuts import render
from scipy.special import softmax
from django.db.models import Avg, Count
from better_profanity import profanity

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

model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")

def analyze_emotions(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    outputs = model(**inputs)
    scores = outputs[0][0].detach().numpy()
    scores = softmax(scores)
    emotions = {
        'anger': scores[0],
        'disgust': scores[1],
        'fear': scores[2],
        'happiness': scores[3],
        'neutral': scores[4],
        'sadness': scores[5],
        'surprise': scores[6]
    }
    return emotions

# Load the profanity word list
profanity.load_censor_words()

def check_profanity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')

        if profanity.contains_profanity(title) or profanity.contains_profanity(description):
            return JsonResponse({'contains_profanity': True})
        else:
            return JsonResponse({'contains_profanity': False})
    return JsonResponse({'contains_profanity': False}, status=400)

def get_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    data = {
        'success': True,
        'status': {
            'id': status.id,
            'title': status.title,
            'description': status.description,
            'plain_description': status.plain_description,
            'created_at': status.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'username': status.user.username,
            'emotion': status.emotion,
        }
    }
    return JsonResponse(data)

@require_POST
def submit_referral(request):
    data = json.loads(request.body)
    try:
        status = Status.objects.get(id=data['status_id'])
        referral = Referral.objects.create(
            status=status,
            referred_by=request.user,
            highlighted_title=data.get('highlighted_title', ''),
            highlighted_description=data.get('highlighted_description', '')
        )
        return JsonResponse({'success': True})
    except Status.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Status not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def save_questionnaire(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question_index = data.get("question_index")
        answer = data.get("answer", "No answer provided")
        response = data.get("response", "No response provided")

        # Define the questions list (ensure it matches the JavaScript)
        questions = [
            "What aspects of your academic life cause you the most stress?",
            "How would you describe your overall emotional state in the past month?",
            "How comfortable do you feel talking to friends or family about your mental health?",
            "How frequently do you experience feelings of anxiety or worry related to school?",
            "How many hours of sleep do you usually get on a school night?",
            "How confident do you feel in your academic abilities?",
            "How do you usually feel about changes in your academic or personal life?",
            "How do you manage your time between schoolwork, extracurricular activities, and relaxation?",
            "How motivated do you feel to complete your academic tasks?",
            "Are you aware of the mental health resources available at your school?",
        ]

        # Fetch the corresponding question text
        question_text = questions[question_index]

        # Save the data into the Questionnaire model
        Questionnaire.objects.create(
            user=request.user,
            question=question_text,
            answer=answer,
            response=response
        )

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        is_bot_message = data.get('is_bot_message')

        if message:
            # Save the message to the database
            ChatMessage.objects.create(
                user=request.user if not is_bot_message else None,
                message=message,
                is_bot_message=is_bot_message,
                created_at=timezone.now()
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No message provided'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def send_chat_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        is_bot_message = data.get('is_bot_message', False)

        if message:
            chat_message = ChatMessage.objects.create(
                user=request.user if not is_bot_message else None,
                message=message,
                is_bot_message=is_bot_message,
                timestamp=timezone.now()
            )
            return JsonResponse({'success': True, 'message_id': chat_message.id})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
def get_chat_messages(request):
    if request.method == 'GET':
        messages = ChatMessage.objects.all().order_by('timestamp')
        message_data = [{
            'id': msg.id,
            'user': msg.user.username if msg.user else 'Bot',
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_bot_message': msg.is_bot_message
        } for msg in messages]
        return JsonResponse({'messages': message_data})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
@require_POST
def refer_status(request, status_id):
    try:
        status = get_object_or_404(Status, id=status_id)
        highlighted_title = request.POST.get('highlightedTitle', '')
        highlighted_description = request.POST.get('highlightedDescription', '')
        referral_reason = request.POST.get('referralReason', '')
        other_reason = request.POST.get('otherReason', '')

        # Save the referral
        referral = Referral.objects.create(
            status=status,
            referred_by=request.user,
            highlighted_title=highlighted_title,
            highlighted_description=highlighted_description,
            referral_reason=referral_reason,
            other_reason=other_reason,
        )

        return JsonResponse({'success': True})
    except Status.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Status not found'}, status=404)

@login_required
@csrf_exempt
def submit_status(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')
            emotion = data.get('emotion')
        else:
            title = request.POST.get('title')
            description = request.POST.get('description')
            emotion = request.POST.get('emotion')
        
        plain_description = strip_html_tags(description)

        # Validate the input fields
        errors = {}
        if not title:
            errors['title'] = 'This field is required.'
        if not description:
            errors['description'] = 'This field is required.'
        if not emotion:
            errors['emotion'] = 'This field is required.'

        # Check for inappropriate words
        if profanity.contains_profanity(title) or profanity.contains_profanity(plain_description):
            errors['profanity'] = 'Your status contains inappropriate language. Please edit and try again.'

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Analyze emotions
        emotions = analyze_emotions(plain_description)

        # Convert emotions to percentages
        emotion_percentages = {key: int(value * 100) for key, value in emotions.items()}

        # Save the status to the database
        status = Status.objects.create(
            user=request.user,
            title=title,
            description=description,
            plain_description=plain_description,
            emotion=emotion,
            anger=emotions['anger'],
            disgust=emotions['disgust'],
            fear=emotions['fear'],
            happiness=emotions['happiness'],
            sadness=emotions['sadness'],
            surprise=emotions['surprise'],
            neutral=emotions['neutral'],
            anger_percentage=emotion_percentages['anger'],
            disgust_percentage=emotion_percentages['disgust'],
            fear_percentage=emotion_percentages['fear'],
            happiness_percentage=emotion_percentages['happiness'],
            sadness_percentage=emotion_percentages['sadness'],
            surprise_percentage=emotion_percentages['surprise'],
            neutral_percentage=emotion_percentages['neutral']
        )

        # Prepare the status data to return
        status_data = {
            'id': status.id,
            'username': request.user.username,
            'avatar_url': request.user.profile.avatar.url if request.user.profile.avatar else None,
            'title': status.title,
            'description': status.plain_description,
            'emotion': status.emotion,
            'created_at': timesince(status.created_at),
            'replies': 0  # Placeholder for replies
        }

        return JsonResponse({'success': True, 'status': status_data, 'message': 'Status shared successfully!'})

    return JsonResponse({'success': False, 'errors': {'non_field_errors': 'Invalid request method'}}, status=400)

@login_required
@csrf_exempt
def add_reply(request, status_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')

        if not text:
            return JsonResponse({'success': False, 'error': 'Reply text is required'}, status=400)

        status = get_object_or_404(Status, id=status_id)
        reply = Reply.objects.create(status=status, user=request.user, text=text)

        return JsonResponse({'success': True, 'reply': {
            'id': reply.id,
            'username': reply.user.username,
            'text': reply.text,
            'created_at': reply.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
def status_detail(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    replies = status.replies.all()
    avatar_url = status.user.profile.avatar.url if status.user.profile.avatar else "/static/images/avatars/placeholder.png"
    return render(request, 'status_detail.html', {'status': status, 'replies': replies, 'avatar_url': avatar_url})

@login_required
@csrf_exempt
def submit_reply(request, status_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            status = get_object_or_404(Status, id=status_id)
            reply = Reply.objects.create(status=status, user=request.user, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@csrf_exempt
def contact_us_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        ContactUs.objects.create(name=name, email=email, subject=subject, message=message)

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
@login_required
def get_all_statuses(request):
    page_size = 100  # Number of statuses per batch
    page_number = int(request.GET.get('page', 1))
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
            'plain_description': status.plain_description,  # Include plain_description
            'description': status.description,  # Include description with formatted text
            'created_at': timesince(status.created_at).split(',')[0],  # Take only the first part
            'replies': status.replies.count(),  # Count the number of replies
            'can_delete': status.user.id == authenticated_user_id
        }
        for status in page_obj
    ]

    return JsonResponse({
        'statuses': statuses_data,
        'has_next': page_obj.has_next()
    })

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