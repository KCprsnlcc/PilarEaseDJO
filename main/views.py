from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from asgiref.sync import async_to_sync
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
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
from .models import Status, Reply, ContactUs, Referral, Questionnaire, CustomUser, EmailHistory, Notification, UserNotificationSettings, ChatMessage, ProfanityWord
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
from .models import Feedback
from .forms import FeedbackForm
from textblob import TextBlob
from django.shortcuts import render
from scipy.special import softmax
from django.db.models import Avg, Count
from better_profanity import profanity
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes  # Replace force_text with force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.conf import settings
from django.templatetags.static import static
from email.mime.image import MIMEImage
from django.db.models import Q 
from django.utils.timezone import make_aware
from django.utils.html import strip_tags
from django.utils.timezone import now
from itrc_tools.models import EnrollmentMasterlist, VerificationRequest
from django.contrib import messages

logger = logging.getLogger(__name__)
CustomUser = get_user_model()

def current_time_view(request):
    tz = pytz.timezone('Asia/Manila')
    current_time = datetime.now(tz)
    return HttpResponse(f"The current time in Manila is: {current_time}")

def home(request):
    return render(request, 'home.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def about_view(request):
    # Fetch the 3 most recent approved testimonials
    approved_feedbacks = Feedback.objects.filter(is_approved=True).order_by('-created_at')[:3]
    return render(request, 'about.html', {'feedbacks': approved_feedbacks})
# Check if username already exists

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
def profile_view(request):
    # Calculate updated statistics
    total_statuses = Status.objects.filter(user=request.user).count()
    total_replies_received = Reply.objects.filter(status__user=request.user).count()

    # Calculate statuses over time for the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    statuses_over_time = (
        Status.objects.filter(user=request.user, created_at__gte=thirty_days_ago)
        .extra({'day': "date(created_at)"})
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    context = {
        'total_statuses': total_statuses,
        'total_replies_received': total_replies_received,
        'statuses_over_time': list(statuses_over_time),  # Convert QuerySet to list for JSON serialization
    }

    return render(request, 'profile.html', context)

@login_required
def get_user_analytics(request):
    # Fetching statuses and replies over the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Aggregating statuses over time
    statuses_over_time = (
        Status.objects.filter(user=request.user, created_at__gte=thirty_days_ago)
        .extra({'day': "date(created_at)"})
        .values('day')
        .annotate(status_count=Count('id'))  # Count the number of statuses per day
        .order_by('day')
    )
    
    # Aggregating replies over time
    replies_over_time = (
        Reply.objects.filter(user=request.user, created_at__gte=thirty_days_ago)
        .extra({'day': "date(created_at)"})
        .values('day')
        .annotate(reply_count=Count('id'))  # Count the number of replies per day
        .order_by('day')
    )
    
    # Creating dictionaries to map dates to counts
    status_date_counts = {item['day'].strftime('%Y-%m-%d'): item['status_count'] for item in statuses_over_time}
    reply_date_counts = {item['day'].strftime('%Y-%m-%d'): item['reply_count'] for item in replies_over_time}

    # Generate the last 30 days' date list
    all_dates = [(timezone.now() - timedelta(days=i)).date() for i in range(29, -1, -1)]
    
    # Prepare the data to include both status and reply counts for each date
    statuses_data = [
        {
            'date': date.strftime('%Y-%m-%d'),
            'status_count': status_date_counts.get(date.strftime('%Y-%m-%d'), 0),
            'reply_count': reply_date_counts.get(date.strftime('%Y-%m-%d'), 0),
        }
        for date in all_dates
    ]

    return JsonResponse({'statuses_over_time': statuses_data})


@login_required
def get_user_statuses(request):
    page_number = request.GET.get('page', 1)
    statuses = Status.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(statuses, 10)  # 10 statuses per page

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    statuses_data = []
    for status in page_obj.object_list:
        statuses_data.append({
            'id': status.id,
            'username': request.user.username,
            'avatar_url': request.user.profile.avatar.url if request.user.profile.avatar else '/static/images/avatars/placeholder.png',
            'title': status.title,
            'description': status.description,
            'created_at': status.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'replies': status.replies.count(),
            'can_edit': status.user == request.user,
        })

    return JsonResponse({
        'statuses': statuses_data,
        'has_next': page_obj.has_next(),
    })
    
@login_required
def get_recent_activity(request):
    page_number = request.GET.get('page', 1)
    user = request.user
    # Fetch replies to user's statuses
    replies = Reply.objects.filter(status__user=user).order_by('-created_at')
    paginator = Paginator(replies, 10)  # 10 activities per page

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    activities_data = []
    for reply in page_obj.object_list:
        activities_data.append({
            'actor': reply.user.username,
            'action': 'replied to',
            'status_title': reply.status.title,
            'timestamp': reply.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return JsonResponse({
        'activities': activities_data,
        'has_next': page_obj.has_next(),
    })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data.get('student_id')
            email = form.cleaned_data.get('email')

            # Check if the student is in the EnrollmentMasterlist
            try:
                EnrollmentMasterlist.objects.get(student_id=student_id)
            except EnrollmentMasterlist.DoesNotExist:
                errors = {
                    'student_id': [
                        {
                            'message': 'Student ID not found in enrollment records.',
                            'code': 'invalid'
                        }
                    ]
                }
                return JsonResponse({'success': False, 'error_message': errors}, status=400)

            user = form.save(commit=False)
            user.is_active = False  # User cannot login until verified
            user.verification_status = 'pending'
            user.save()
            VerificationRequest.objects.create(user=user)

            # Instead of messages.info, return a JSON response
            return JsonResponse({
                'success': True,
                'message': 'Your registration is pending verification.',
                'redirect_url': '/login/'
            })
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({'success': False, 'error_message': errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'base.html', {'register_form': form, 'show_register_modal': False})
def request_email_change(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_email = data.get('new_email')
            user = request.user

            # Check if the new email is provided
            if not new_email:
                return JsonResponse({'success': False, 'error': 'New email is required.'})

            # Check if the new email is the same as the current email
            if user.email == new_email:
                return JsonResponse({'success': False, 'error': 'This is already your current email address.'})

            # Check if the new email was used previously
            if EmailHistory.objects.filter(Q(user=user) & Q(email=new_email)).exists():
                return JsonResponse({'success': False, 'error': 'You have already used this email previously. Please choose a different one.'})

            # Check if the new email is already in use by another user
            if CustomUser.objects.filter(email=new_email).exists():
                return JsonResponse({'success': False, 'error': 'This email is already in use by another user.'})

            # Generate email change token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Store the email change request time (to verify expiry later)
            user.profile.email_change_requested_at = now()
            user.profile.new_email = new_email  # Temporarily store the new email in the profile
            user.profile.save()

            # Generate email verification link
            verification_link = request.build_absolute_uri(f'/verify_email_change/{uid}/{token}/{new_email}/')

            # Send the verification email to the new email address
            email_subject = 'Confirm Your New Email'
            email_html_content = render_to_string('change_email.html', {
                'user': user,
                'verification_link': verification_link,
            })
            email_text_content = strip_tags(email_html_content)

            email_message = EmailMultiAlternatives(
                email_subject,
                email_text_content,
                'PilarEase <no-reply@pilarease.com>',
                [new_email],  # Send to the new email address
            )
            email_message.attach_alternative(email_html_content, "text/html")
            email_message.send()

            return JsonResponse({'success': True, 'message': 'Verification link sent.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid data format.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def request_email_verification(request):
    if request.method == 'POST':
        user = request.user
        email = user.email
        if not user.profile.is_email_verified:
            # Generate a verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            verification_link = request.build_absolute_uri(f"/verify_email/{uid}/{token}/")

            # Render the email content
            email_subject = "Email Verification"
            email_html_content = render_to_string("email_verification.html", {
                "user": user,
                "verification_link": verification_link,
                "site_name": "PilarEase",
            })
            email_text_content = strip_tags(email_html_content)

            # Create the email message object
            email_message = EmailMultiAlternatives(
                email_subject,
                email_text_content,
                'PilarEase <no-reply@pilarease.com>',
                [user.email],
            )
            email_message.attach_alternative(email_html_content, "text/html")

            # Send the email
            email_message.send()

            return JsonResponse({'success': True, 'message': 'Verification email sent!'})
        else:
            return JsonResponse({'success': False, 'error': 'Email already verified.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

TOKEN_EXPIRY_MINUTES = 60  # Set token expiry time to 60 minutes

def verify_email_change(request, uidb64, token, new_email):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            token_age = now() - user.profile.email_change_requested_at

            if token_age > timedelta(minutes=TOKEN_EXPIRY_MINUTES):
                return render(request, "change_email_complete.html", {
                    "invalid": True,
                    "message": "The verification link has expired. Please request a new email change."
                })

            # Ensure the new email is still available (not taken by another user)
            if CustomUser.objects.filter(email=new_email).exists():
                return render(request, "change_email_complete.html", {
                    "invalid": True,
                    "message": "This email is already in use by another user. Please choose a different email."
                })

            # Add current email to email history before changing
            EmailHistory.objects.create(user=user, email=user.email)

            # Update the user's email to the new email and mark it as verified
            user.email = new_email
            user.profile.is_email_verified = True  # Automatically verify the new email
            user.save()

            return render(request, "change_email_complete.html", {"verified": True})

        else:
            return render(request, "change_email_complete.html", {
                "invalid": True,
                "message": "The verification link is invalid. Please request a new email change."
            })

    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return render(request, "change_email_complete.html", {
            "invalid": True,
            "message": "Invalid verification link or user not found. Please try again."
        })
        return render(request, "change_email_complete.html", {"invalid": True})
    
def check_email_verification(request):
    user = request.user
    if user.is_authenticated:
        is_verified = user.profile.is_email_verified
        return JsonResponse({'is_verified': is_verified})
    return JsonResponse({'error': 'User not authenticated'}, status=403)

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            token_age = now() - user.profile.email_verification_requested_at
            logger.info(f"Token age: {token_age}, Token valid: {default_token_generator.check_token(user, token)}")

            if token_age > timedelta(minutes=TOKEN_EXPIRY_MINUTES):
                return render(request, "email_verification_complete.html", {
                    "invalid": True,
                    "message": "The verification link has expired. Please request a new verification link."
                })

            # Mark email as verified if it is not already verified
            if not user.profile.is_email_verified:
                user.profile.is_email_verified = True
                user.profile.save()

            return render(request, "email_verification_complete.html", {"verified": True})
        else:
            return render(request, "email_verification_complete.html", {
                "invalid": True,
                "message": "The verification link is invalid. Please request a new verification link."
            })
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return render(request, "email_verification_complete.html", {
            "invalid": True,
            "message": "Invalid verification link or user not found. Please try again."
        })
    
def send_verification_email(request):
    if request.method == 'POST':
        user = request.user
        email = user.email
        if not user.profile.is_email_verified:
            # Set the email_verification_requested_at timestamp
            user.profile.email_verification_requested_at = now()
            user.profile.save()

            # Generate a verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            verification_link = request.build_absolute_uri(f"/verify_email/{uid}/{token}/")

            # Render the email content
            email_subject = "Email Verification"
            email_html_content = render_to_string("email_verification.html", {
                "user": user,
                "verification_link": verification_link,
                "site_name": "PilarEase",
            })
            email_text_content = strip_tags(email_html_content)

            # Create the email message object
            email_message = EmailMultiAlternatives(
                email_subject,
                email_text_content,
                'PilarEase <no-reply@pilarease.com>',
                [user.email],
            )
            email_message.attach_alternative(email_html_content, "text/html")

            # Send the email
            email_message.send()

            return JsonResponse({'success': True, 'message': 'Verification email sent!'})
        else:
            return JsonResponse({'success': False, 'error': 'Email already verified.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'success': True, 'redirect_url': '/'})
                else:
                    # User account is inactive (pending verification)
                    error_message = {
                        '__all__': [
                            {
                                'message': 'Your account is pending verification.',
                                'code': 'inactive'
                            }
                        ]
                    }
                    return JsonResponse({'success': False, 'error_message': error_message}, status=400)
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

def custom_password_reset_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        last_sent = request.session.get('last_password_reset_email', None)
        # Check if the last email was sent less than 3 minutes ago
        if last_sent:
            last_sent_time = timezone.datetime.strptime(last_sent, "%Y-%m-%d %H:%M:%S.%f%z")
            if timezone.now() - last_sent_time < timedelta(minutes=3):
                return JsonResponse({
                    "success": False, 
                    "error": "You can request a new password reset link every 3 minutes."
                })
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = request.build_absolute_uri(f"/reset/{uid}/{token}/")

            # Render email content
            email_subject = "Password Reset Requested"
            email_html_content = render_to_string("password_reset_email.html", {
                "user": user,
                "reset_link": reset_link,
                "site_name": "PilarEase",
            })
            email_text_content = strip_tags(email_html_content)

            # Create the email message object
            email_message = EmailMultiAlternatives(
                email_subject,
                email_text_content,
                'PilarEase <no-reply@pilarease.com>',  # Use a no-reply email address here
                [user.email],
            )
            email_message.reply_to = ['support@pilarease.com']
            email_message.attach_alternative(email_html_content, "text/html")

            # Send the email
            email_message.send()

            # Store the current time in session to track the cooldown for this email
            request.session[f'last_password_reset_email_{email}'] = str(timezone.now())

            return JsonResponse({"success": True, "message": "Password reset link has been sent to your email."})
        except CustomUser.DoesNotExist:
            return JsonResponse({"success": False, "error": "No user is associated with this email address."})
    return render(request, "password_reset_form.html")

def custom_password_reset_done_view(request):
    return render(request, "password_reset_done.html")

def custom_password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                new_password = request.POST.get("new_password")
                new_password_confirm = request.POST.get("new_password_confirm")

                if new_password and new_password == new_password_confirm:
                    user.set_password(new_password)
                    user.save()
                    return redirect("password_reset_complete")
                else:
                    # Handle password mismatch
                    return render(
                        request, 
                        "password_reset_confirm.html", 
                        {"validlink": True, "user": user, "error": "Passwords do not match."}
                    )
            return render(request, "password_reset_confirm.html", {"validlink": True, "user": user})
        else:
            return render(request, "password_reset_confirm.html", {"validlink": False})
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return render(request, "password_reset_confirm.html", {"validlink": False})

def custom_password_reset_complete_view(request):
    return render(request, "password_reset_complete.html")

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

def contains_custom_profanity(text):
    """Check if the text contains any custom profanities."""
    custom_profanities = load_custom_profanities()
    for profanity_word in custom_profanities:
        if re.search(rf'\b{profanity_word}\b', text, re.IGNORECASE):
            return True
    return False

@csrf_exempt
def check_profanity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title', '')
        description = data.get('description', '')

        # Check using custom profanity list from the database
        custom_profanity_check = contains_custom_profanity_by_lines(title) or contains_custom_profanity_by_lines(description)

        if custom_profanity_check:
            return JsonResponse({'contains_profanity': True})
        else:
            return JsonResponse({'contains_profanity': False})
    
    return JsonResponse({'contains_profanity': False}, status=400)

def contains_custom_profanity_by_lines(text):
    """Check each line of the input text for profanities stored in the database."""
    lines = text.splitlines()
    
    # Query the database for the profanity words stored in the `ProfanityWord` model
    try:
        profanity_entry = ProfanityWord.objects.get(id=1)
        custom_profanities = profanity_entry.word_list
    except ProfanityWord.DoesNotExist:
        return False  # If the profanity list isn't set, return False by default

    # Check each line for profane words
    for line in lines:
        for profanity_word in custom_profanities:
            if re.search(rf'\b{profanity_word}\b', line, re.IGNORECASE):
                return True
    return False

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

        # Return success response to the user
        return JsonResponse({'success': True, 'status': status_data, 'message': 'Status shared successfully!'})

    return JsonResponse({'success': False, 'errors': {'non_field_errors': 'Invalid request method'}}, status=400)

def format_timestamp(timestamp):
    now = timezone.now()
    diff = now - timestamp

    seconds = diff.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    weeks = days / 7

    if seconds < 60:
        return f"{int(seconds)}s ago"
    elif minutes < 60:
        return f"{int(minutes)}m ago"
    elif hours < 24:
        return f"{int(hours)}hr ago"
    elif days < 7:
        return f"{int(days)}d ago"
    else:
        return f"{int(weeks)}w ago"

@login_required
def fetch_notifications(request):
    page_number = request.GET.get('page', 1)
    notifications = []

    # Set the 7-week limit
    seven_weeks_ago = timezone.now() - timedelta(weeks=7)

    # Fetch user statuses created within the last 7 weeks
    user_statuses = Status.objects.filter(user=request.user, created_at__gte=seven_weeks_ago)

    # 1. Add notifications for statuses
    for status in user_statuses:
        # Create or get a notification entry for the status
        notification, created = Notification.objects.get_or_create(
            user=request.user, 
            status=status,
            defaults={'is_read': False}
        )

        # Add notification for the uploaded status
        notifications.append({
            'id': f"status_{status.id}",
            'status_id': status.id,
            'message': "You uploaded a status. Click to view it.",
            'link': f'/status/{status.id}/',
            'avatar': request.user.profile.avatar.url if request.user.profile.avatar else '/static/images/avatars/placeholder.png',
            'timestamp': status.created_at,  # Raw timestamp (sorting will be based on this)
            'is_read': notification.is_read
        })

        # Fetch replies for the status
        status_replies = Reply.objects.filter(status=status, created_at__gte=seven_weeks_ago).exclude(user=request.user).order_by('-created_at')
        unique_users = {reply.user for reply in status_replies}  # Ensure unique users

        if unique_users:
            # Fetch only the latest reply from unique users
            latest_unique_replies = list(status_replies.filter(user__in=unique_users))[:2]
            latest_usernames = [reply.user.username for reply in latest_unique_replies]
            latest_user_avatar = latest_unique_replies[0].user.profile.avatar.url if latest_unique_replies[0].user.profile.avatar else '/static/images/avatars/placeholder.png'

            # Create the appropriate message based on the number of unique users
            if len(unique_users) == 1:
                message = f"{latest_usernames[0]} replied to your status, click to see it."
            elif len(unique_users) == 2:
                message = f"{latest_usernames[0]} and {latest_usernames[1]} replied to your status, click to see it."
            elif len(unique_users) > 2:
                message = f"{latest_usernames[0]}, {latest_usernames[1]} and others replied to your status, click to see it."

            # Create or get a notification entry for the replies
            notification, created = Notification.objects.get_or_create(
                user=request.user, 
                status=status,
                defaults={'is_read': False}
            )

            # Add reply notifications
            notifications.append({
                'id': f"replies_{status.id}",
                'message': message,
                'link': f'/status/{status.id}/',
                'avatar': latest_user_avatar,
                'timestamp': latest_unique_replies[0].created_at,  # Raw timestamp (sorting will be based on this)
                'is_read': notification.is_read
            })

    # Sort the notifications by timestamp in descending order
    notifications.sort(key=lambda x: x['timestamp'], reverse=True)

    # Paginate notifications (5 per page)
    paginator = Paginator(notifications, 5)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Convert the raw timestamps to human-readable format after sorting
    for notification in page_obj.object_list:
        notification['timestamp'] = format_timestamp(notification['timestamp'])

    return JsonResponse({
        'notifications': page_obj.object_list,
        'total_pages': paginator.num_pages
    })

@login_required
@csrf_exempt
def mark_notification_as_read(request, notification_id):
    try:
        # Fetch the notification using the correct notification ID
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()

        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)
    
@login_required
def mark_notification_button_clicked(request):
    try:
        # Mark the notification button as clicked in user settings
        user_settings, created = UserNotificationSettings.objects.get_or_create(user=request.user)
        user_settings.has_clicked_notification = True  # Mark as clicked
        user_settings.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def check_notification_status(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    user_settings, created = UserNotificationSettings.objects.get_or_create(user=request.user)
    has_unread_notifications = notifications.exists()
    
    return JsonResponse({
        'has_unread_notifications': has_unread_notifications,
        'has_clicked_notification': user_settings.has_clicked_notification
    })

@login_required
@csrf_exempt
def add_reply(request, status_id, parent_reply_id=None):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        
        if not text:
            return JsonResponse({'success': False, 'error': 'Reply text is required'}, status=400)

 # Extract mentioned usernames
        mentioned_usernames = re.findall(r'@(\w+)', text)
        mentioned_users = CustomUser.objects.filter(username__in=mentioned_usernames)
        # Handle notifications for mentioned users
        for user in mentioned_users:
            if user != request.user:
                # Create a notification or send an email
                pass  # Implement your notification logic here
            
        status = get_object_or_404(Status, id=status_id)
        parent_reply = None
        if parent_reply_id:
            parent_reply = get_object_or_404(Reply, id=parent_reply_id)

            # Check nesting level
            nesting_level = 1
            current_reply = parent_reply
            while current_reply.parent_reply is not None:
                nesting_level += 1
                current_reply = current_reply.parent_reply

            if nesting_level >= 3:
                # Do not nest further
                parent_reply = None

        reply = Reply.objects.create(
            status=status,
            user=request.user,
            text=text,
            parent_reply=parent_reply  # If it's a nested reply, this will not be None
        )

        # Format the timestamp for the reply
        created_at = format_timestamp(reply.created_at)

        # Return a success response with the reply details
        return JsonResponse({
            'success': True,
            'reply': {
                'id': reply.id,
                'username': reply.user.username,
                'avatar_url': reply.user.profile.avatar.url if reply.user.profile.avatar else '/static/images/avatars/placeholder.png',
                'text': reply.text,
                'created_at': created_at,  # Formatted timestamp
                'label': 'Reply'
            }
        })

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
def status_detail(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    replies = status.replies.filter(parent_reply__isnull=True).all()  # Level 1

    # Fetch nested replies up to 3 levels
    formatted_replies = []
    for reply in replies:
        level2_nested_replies = []
        for nested_reply in reply.nested_replies.all():  # Level 2
            level3_nested_replies = []
            for nested_nested_reply in nested_reply.nested_replies.all():  # Level 3
                level3_nested_replies.append({
                    'id': nested_nested_reply.id,
                    'username': nested_nested_reply.user.username,
                    'avatar_url': nested_nested_reply.user.profile.avatar.url if nested_nested_reply.user.profile.avatar else '/static/images/avatars/placeholder.png',
                    'text': nested_nested_reply.text,
                    'created_at': format_timestamp(nested_nested_reply.created_at),
                })

            level2_nested_replies.append({
                'id': nested_reply.id,
                'username': nested_reply.user.username,
                'avatar_url': nested_reply.user.profile.avatar.url if nested_reply.user.profile.avatar else '/static/images/avatars/placeholder.png',
                'text': nested_reply.text,
                'created_at': format_timestamp(nested_reply.created_at),
                'nested_replies': level3_nested_replies,
            })

        formatted_replies.append({
            'id': reply.id,
            'username': reply.user.username,
            'avatar_url': reply.user.profile.avatar.url if reply.user.profile.avatar else '/static/images/avatars/placeholder.png',
            'text': reply.text,
            'created_at': format_timestamp(reply.created_at),
            'nested_replies': level2_nested_replies,
        })

    avatar_url = status.user.profile.avatar.url if status.user.profile.avatar else "/static/images/avatars/placeholder.png"
    
     # Fetch similar statuses (excluding the current one)
    similar_statuses = Status.objects.filter(emotion=status.emotion).exclude(id=status.id)[:3]
    
    return render(request, 'status_detail.html', {
        'status': status,
        'replies': formatted_replies,
        'avatar_url': avatar_url,
        'similar_statuses': similar_statuses,  # Pass similar statuses to the template
    })
    
@login_required
def get_usernames(request):
    search_term = request.GET.get('q', '')
    # Exclude the current user from the list if desired
    users = CustomUser.objects.filter(username__icontains=search_term).exclude(id=request.user.id)[:10]
    usernames = list(users.values_list('username', flat=True))
    return JsonResponse({'usernames': usernames})

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
def statuses_over_time(request):
    # Calculate statuses per week for the last 12 weeks
    today = timezone.now().date()
    weeks = [today - timedelta(weeks=i) for i in range(12)]
    weeks.reverse()  # Oldest to newest

    labels = [week.strftime('%b %d') for week in weeks]
    values = []
    for week in weeks:
        start = week
        end = week + timedelta(days=6)
        count = Status.objects.filter(user=request.user, created_at__date__gte=start, created_at__date__lte=end).count()
        values.append(count)

    return JsonResponse({'labels': labels, 'values': values})

@login_required
def reply_distribution(request):
    # Calculate distribution of replies by emotion
    statuses = Status.objects.filter(user=request.user)
    emotion_counts = statuses.values('emotion').annotate(count=Count('id'))

    labels = [item['emotion'].capitalize() for item in emotion_counts]
    values = [item['count'] for item in emotion_counts]

    return JsonResponse({'labels': labels, 'values': values})
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
        'bio': user_profile.bio,  # Include bio in the response
    }
    return JsonResponse(data)

@login_required
@csrf_exempt
def update_user_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        contact_number = data.get('contact_number')
        academic_year_level = data.get('academic_year_level')
        user = request.user
        response_data = {'success': True, 'errors': {}}
        
        # Check if the username or email already exists for another user
        if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
            response_data['success'] = False
            response_data['errors']['username'] = 'Username already exists.'

        # Update the user details if there are no errors
        if response_data['success']:
            user.username = username
            user.contact_number = contact_number
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

def submit_feedback(request):
    if request.method == 'POST':
        # Assuming the user is authenticated
        message = request.POST.get('message', '')

        if message:
            feedback = Feedback(user=request.user, message=message)
            
            # Sentiment analysis with TextBlob
            blob = TextBlob(message)
            feedback.sentiment_score = blob.sentiment.polarity

            # Approve feedback if sentiment score is positive
            if feedback.sentiment_score > 0.1:
                feedback.is_approved = True

            feedback.save()

            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'errors': 'Invalid input'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'Logout successful!', 'redirect_url': '/'})
    return redirect('home')