from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from asgiref.sync import async_to_sync
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from datetime import datetime
from django.db import IntegrityError
import pytz
import json
import uuid
from django.db import transaction, IntegrityError
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AvatarUploadForm
from django.contrib.auth.hashers import check_password
from django.core.files.storage import default_storage
from itrc_tools.models import EnrollmentMasterlist, SystemSetting, AuditLog, Notification_System
from django.core.files.base import ContentFile
from .models import UserProfile
import logging
from .models import UserSession  
from django.contrib.sessions.models import Session
from itrc_tools.models import AuditLog
from PIL import Image
from io import BytesIO
import os
from .models import Status, Reply, Emoji, ContactUs, Referral, Questionnaire, NotificationCounselor, CustomUser, EmailHistory, Notification, UserNotificationSettings, ChatMessage, ProfanityWord, QuestionnaireProgress
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
from itrc_tools.models import SystemSetting
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
    categories = [
        ("Smileys & Emotion", "fa-solid fa-face-smile"),
        ("People & Body", "fa-solid fa-users"),
        ("Animals & Nature", "fa-solid fa-leaf"),
        ("Food & Drink", "fa-solid fa-mug-hot"),
        ("Activities", "fa-solid fa-futbol"),
        ("Travel & Places", "fa-solid fa-location-dot"),
        ("Objects", "fa-solid fa-lightbulb"),
        ("Symbols", "fa-solid fa-heart"),
        ("Flags", "fa-solid fa-flag")
    ]

    # Get selected category and search query from GET parameters
    category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')

    context = {
        'categories': categories,
        'category': category,
        'search_query': search_query
    }

    return render(request, 'home.html', context)

def contact_us(request):
    return render(request, 'contact_us.html')

def about_view(request):
    # Fetch the 3 most recent approved testimonials
    approved_feedbacks = Feedback.objects.filter(is_approved=True).order_by('-created_at')[:3]
    return render(request, 'about.html', {'feedbacks': approved_feedbacks})
# Check if username already exists

# Predefined questions and answers
QUESTIONS = [
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

ANSWERS = [
    [
      "Managing multiple assignments and deadlines.",
      "Understanding difficult subjects or topics.",
      "Balancing academics with extracurricular activities.",
    ],
    [
      "Generally positive, with only occasional low moods.",
      "Mixed, with frequent ups and downs.",
      "Often stressed or anxious.",
    ],
    [
      "Very comfortable, I often share how I’m feeling.",
      "Somewhat comfortable, I share occasionally.",
      "Not comfortable, I usually keep things to myself.",
    ],
    [
      "Almost daily, it’s a constant presence.",
      "Occasionally, but only around stressful times like exams.",
      "Rarely, I don’t get anxious easily.",
    ],
    [
      "Less than 6 hours, I often stay up late.",
      "Between 6 and 8 hours, it varies.",
      "More than 8 hours, I prioritize my sleep.",
    ],
    [
      "Very confident, I believe in my abilities.",
      "Somewhat confident, but I have doubts sometimes.",
      "Not very confident, I often worry about my performance.",
    ],
    [
      "Excited and ready to adapt.",
      "Nervous but willing to adjust.",
      "Stressed and resistant to change.",
    ],
    [
      "I create a schedule and stick to it as much as possible.",
      "I try to balance things, but it’s a challenge.",
      "I often struggle to manage my time effectively.",
    ],
    [
      "Highly motivated, I’m eager to succeed.",
      "Moderately motivated, but it depends on the task.",
      "Often unmotivated, I struggle to find the drive.",
    ],
    [
      "Yes, I know where to find help if I need it.",
      "Somewhat, I’ve heard of some resources but haven’t explored them.",
      "No, I’m not aware of the available resources.",
    ],
]

RESPONSES = [
    [
      "Managing multiple assignments can lead to significant stress, which can impact your mental health. It's important to develop strategies to manage this workload to protect your well-being.",
      "Struggling with difficult subjects can cause stress and anxiety. Seeking help or using different study methods can reduce these feelings and improve your mental health.",
      "Balancing academics and extracurriculars can be stressful and may overwhelm your mental health. Finding a healthy balance is key to maintaining your mental well-being.",
    ],
    [
      "It's great to hear that you've been feeling generally positive. Maintaining a positive emotional state is important for good mental health, so keep focusing on what keeps you feeling well.",
      "Experiencing frequent ups and downs can be challenging for your mental health. It might be helpful to explore techniques to stabilize your emotions and support your well-being.",
      "Feeling stressed or anxious often can take a toll on your mental health. It's important to address these feelings and find ways to manage them to protect your mental and emotional well-being.",
    ],
    [
      "It’s excellent that you feel comfortable discussing your mental health with others. Having a support system is crucial for maintaining good mental health.",
      "It’s good that you share your feelings sometimes. Being open about your mental health can provide relief and support, which are important for emotional well-being.",
      "Keeping your feelings to yourself can lead to increased stress and affect your mental health. Consider finding a trusted person to talk to, as sharing can be very beneficial.",
    ],
    [
      "Experiencing daily anxiety can significantly impact your mental health. It's important to seek ways to reduce this anxiety, as prolonged stress can have serious effects on your well-being.",
      "Feeling anxious during stressful times like exams is common, but managing this anxiety is key to protecting your mental health during these periods.",
      "It's great that you rarely experience anxiety. Maintaining this level of calm is beneficial for your mental health, and it’s important to continue practicing whatever keeps you feeling this way.",
    ],
    [
      "Getting less than 6 hours of sleep can negatively affect your mental health, leading to increased stress and reduced emotional resilience. Prioritizing sleep is crucial for your well-being.",
      "Getting between 6 and 8 hours of sleep is important, but inconsistency can impact your mental health. A regular sleep routine can improve your emotional stability and reduce stress.",
      "Prioritizing sleep is one of the best things you can do for your mental health. It helps maintain emotional balance and resilience, which are key to handling stress.",
    ],
    [
      "Feeling confident in your abilities is excellent for your mental health. It can reduce anxiety and stress, contributing to a more positive and balanced state of mind.",
      "Having some doubts is normal, but too much self-doubt can negatively impact your mental health. Building confidence through small successes can help improve your overall well-being.",
      "Constant worry about your performance can lead to anxiety and stress, affecting your mental health. It's important to address these worries and work on building self-confidence.",
    ],
    [
      "Being excited about change is a positive sign for your mental health. Adaptability and a positive outlook can help you manage stress and maintain emotional well-being.",
      "It’s normal to feel nervous about change, but being willing to adjust is important for your mental health. Embracing change gradually can help reduce stress and anxiety.",
      "Resistance to change can cause stress, which may impact your mental health. Finding ways to cope with change is crucial for maintaining emotional stability.",
    ],
    [
      "Having a schedule and sticking to it is excellent for your mental health. It helps reduce stress and ensures you have time for relaxation, which is crucial for emotional well-being.",
      "Balancing your responsibilities can be challenging and impact your mental health. Developing better time management skills can reduce stress and improve your overall well-being.",
      "Struggling with time management can lead to stress and affect your mental health. Working on these skills can help you feel more in control and reduce anxiety.",
    ],
    [
      "High motivation is a great indicator of good mental health. Staying motivated helps you manage stress and keep a positive outlook.",
      "It's normal for motivation to vary, but staying engaged in your tasks can support your mental health by providing a sense of accomplishment.",
      "Struggling with motivation can be a sign of mental fatigue or stress. It’s important to address these feelings to prevent them from negatively impacting your mental health.",
    ],
    [
      "It’s great that you’re aware of the mental health resources available. Knowing where to get help is crucial for maintaining your mental well-being.",
      "It’s good that you’re somewhat aware, but exploring these resources further can ensure you have the support you need when challenges arise.",
      "It’s important to be informed about mental health resources, as they can provide crucial support when needed. Taking the time to learn about them can make a big difference.",
    ],
]

@login_required
def get_chat_history(request):
    try:
        page = int(request.GET.get('page', 1))
        page_size = 10  # Define how many messages per page

        # Fetch chat messages including bot messages
        chat_messages = ChatMessage.objects.filter(
            Q(user=request.user) | Q(is_bot_message=True)
        ).order_by('-timestamp')

        paginator = Paginator(chat_messages, page_size)
        try:
            chat_page = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            return JsonResponse({
                'chat_history': [],
                'awaiting_answer': False,
                'current_question_index': None,
                'is_chat_empty': not chat_messages.exists(),
                'last_message_type': None,
                'end_of_questions': False,
                'total_messages': chat_messages.count(),
                'total_pages': paginator.num_pages,
                'show_greeting': not chat_messages.exists()  # Flag to show greeting message when chat is empty
            })

        chat_history = []
        awaiting_answer = False
        current_question_index = None
        end_of_questions = False

        for message in chat_page.object_list:
            chat_history.append({
                'message': message.message,
                'sender': 'bot' if message.is_bot_message else 'user',
                'message_type': message.message_type,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'question_index': message.question_index
            })
            if message.message_type == 'question' and not awaiting_answer:
                awaiting_answer = True
                current_question_index = message.question_index

            if message.message_type == 'bot_message' and "Would you like to talk to a counselor?" in message.message:
                end_of_questions = True

        last_message = chat_messages.first() if chat_messages.exists() else None
        last_message_type = last_message.message_type if last_message else None
        is_chat_empty = not chat_messages.exists()

        return JsonResponse({
            'chat_history': chat_history,
            'awaiting_answer': awaiting_answer,
            'current_question_index': current_question_index,
            'is_chat_empty': is_chat_empty,
            'last_message_type': last_message_type,
            'end_of_questions': end_of_questions,
            'total_messages': chat_messages.count(),
            'total_pages': paginator.num_pages,
            'show_greeting': is_chat_empty  # Flag to show greeting message when chat is empty
        })

    except Exception as e:
        logger.error(f"Error fetching chat history for user '{request.user.username}': {str(e)}")
        return JsonResponse({'success': False, 'error': 'Failed to fetch chat history.'}, status=500)
@login_required
def start_chat(request):
    try:
        data = json.loads(request.body)
        logger.debug(f"Received data for start_chat: {data}")

        # Check if "Start" command was received
        user_message = data.get("message", "").strip()
        if user_message == "start":
            answer_id = data.get('answer_id', str(uuid.uuid4()))
            # Save user message ("Start") to ChatMessage
            user_message_obj = ChatMessage.objects.create(
                user=request.user,
                message="Start",
                is_bot_message=False,
                message_type='user_message'
            )
            progress, created = QuestionnaireProgress.objects.get_or_create(user=request.user)
            if progress.completed:
                return JsonResponse({'success': False, 'error': 'You have already completed the questionnaire.'}, status=400)

            # Reset progress to start the questionnaire
            progress.last_question_index = 0
            progress.completed = False
            progress.save()

            # Fetch the first question
            question_index = progress.last_question_index
            question_text = QUESTIONS[question_index]
            answer_options = ANSWERS[question_index]

            # Save the first question as a bot message
            bot_message = ChatMessage.objects.create(
                user=request.user,
                message=question_text,
                is_bot_message=True,
                message_type='question',
                question_index=question_index
            )
            logger.debug(f"Sent first question (index {question_index}): {question_text}")

            return JsonResponse({
                'success': True,
                'question_index': question_index,
                'question': question_text,
                'answer_options': answer_options,  # Include answer options here
                'simulate_typing': True
            })
        else:
            # Handle unexpected messages gracefully
            bot_message = "I'm sorry, I didn't understand that. Please type 'Start' to begin the questionnaire."
            ChatMessage.objects.create(
                user=request.user,
                message=bot_message,
                is_bot_message=True,
                message_type='bot_message'
            )
            logger.info(f"User '{request.user.username}' sent an unrecognized message: '{user_message}'. Prompted to type 'Start'.")
            return JsonResponse({'success': False, 'error': 'No action taken.', 'message': bot_message}, status=400)

    except json.JSONDecodeError:
        logger.error(f"JSON decoding error in start_chat view for user '{request.user.username}'.")
        return JsonResponse({'success': False, 'error': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in start_chat view for user '{request.user.username}': {str(e)}")
        return JsonResponse({'success': False, 'error': 'Failed to start chat session. Please try again.'}, status=500)
@login_required
@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')

            if not user_message:
                logger.warning("No message provided in request body.")
                return JsonResponse({'success': False, 'error': 'No message provided.'}, status=400)

            # Log received user message
            logger.info(f"Received message from user '{request.user.username}': {user_message}")

            # Save user message to ChatMessage
            ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                is_bot_message=False,
                message_type='user_message'
            )

            # Handle "Start" command
            if user_message.lower() == 'start':
                logger.info(f"User '{request.user.username}' initiated the 'Start' command.")
                try:
                    # Get or initialize QuestionnaireProgress
                    progress, created = QuestionnaireProgress.objects.get_or_create(
                        user=request.user, defaults={'last_question_index': -1}
                    )

                    # Set the first question index
                    next_question_index = progress.last_question_index + 1

                    if next_question_index < len(QUESTIONS):
                        # Send the first question
                        question_text = QUESTIONS[next_question_index]
                        ChatMessage.objects.create(
                            user=request.user,
                            message=question_text,
                            is_bot_message=True,
                            message_type='question',
                            question_index=next_question_index
                        )

                        # Update progress
                        progress.last_question_index = next_question_index
                        progress.save()

                        logger.info(f"Sent question {next_question_index} to user '{request.user.username}': {question_text}")
                        return JsonResponse({
                            'success': True,
                            'message': question_text,
                            'question_index': next_question_index,
                            'simulate_typing': True  # Indicate that simulated typing should be triggered
                        })
                    else:
                        # All questions have been asked
                        final_bot_message = "Thank you for completing the questionnaire! Would you like to talk to a counselor?"
                        ChatMessage.objects.create(
                            user=request.user,
                            message=final_bot_message,
                            is_bot_message=True,
                            message_type='bot_message',
                            timestamp=timezone.now()
                        )
                        logger.info(f"User '{request.user.username}' completed all questions.")
                        return JsonResponse({
                            'success': True,
                            'message': final_bot_message,
                            'end_of_questions': True
                        })
                except Exception as e:
                    logger.error(f"Error processing 'Start' command for user '{request.user.username}': {str(e)}")
                    return JsonResponse({'success': False, 'error': 'Failed to start the questionnaire. Please try again.'}, status=500)

            # Handle other responses or commands after "Start"
            elif user_message.lower() == 'not yet':
                bot_message = "No worries, take your time."
                ChatMessage.objects.create(
                    user=request.user,
                    message=bot_message,
                    is_bot_message=True,
                    message_type='bot_message'
                )
                logger.info(f"User '{request.user.username}' chose 'Not Yet'. Sent response: {bot_message}")
                return JsonResponse({'success': True, 'message': bot_message})
            else:
                bot_message = "I'm here to help whenever you're ready."
                ChatMessage.objects.create(
                    user=request.user,
                    message=bot_message,
                    is_bot_message=True,
                    message_type='bot_message'
                )
                logger.info(f"User '{request.user.username}' sent an unrecognized command. Responded with help message.")
                return JsonResponse({'success': True, 'message': bot_message})

        except IntegrityError as ie:
            logger.error(f"IntegrityError in chat_view for user '{request.user.username}': {str(ie)}")
            return JsonResponse({'success': False, 'error': 'An integrity error occurred. Please try again.'}, status=500)
        except Exception as e:
            logger.error(f"Unexpected error in chat_view for user '{request.user.username}': {str(e)}")
            return JsonResponse({'success': False, 'error': 'Failed to process your answer. Please try again.'}, status=500)

    logger.warning("Invalid request method for chat_view.")
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@login_required
def get_question(request, question_index):
    try:
        question_text = QUESTIONS[question_index]
        # Save bot message
        ChatMessage.objects.create(
            user=request.user,
            message=question_text,
            is_bot_message=True,
            message_type='question',
            question_index=question_index
        )
        return JsonResponse({'success': True, 'question': question_text})
    except IndexError:
        return JsonResponse({'success': False, 'error': 'Invalid question index.'})

@login_required
def get_answer_options(request, question_index):
    try:
        answer_options = ANSWERS[question_index]
        return JsonResponse({'success': True, 'answer_options': answer_options})
    except IndexError:
        return JsonResponse({'success': False, 'error': 'Invalid question index.'})

@require_POST
@login_required
def submit_answer(request):
    """
    Handles the submission of answers in the questionnaire.
    Generates a response based on the chosen answer, saves it to the database, and prepares it for restoration.
    """
    try:
        data = json.loads(request.body)
        question_index = data.get('question_index')
        answer_text = data.get('answer_text')
        answer_id = data.get('answer_id')  # UUID expected

        # Validate required fields
        missing_fields = []
        if question_index is None:
            missing_fields.append('question_index')
        if answer_text is None:
            missing_fields.append('answer_text')
        if answer_id is None:
            missing_fields.append('answer_id')

        if missing_fields:
            error_message = f"Missing required fields: {', '.join(missing_fields)}."
            logger.warning(f"User {request.user.username}: {error_message}")
            return JsonResponse({'success': False, 'error': error_message}, status=400)

        # Validate that question_index is an integer
        if not isinstance(question_index, int):
            error_message = 'Invalid question_index. It must be an integer.'
            logger.warning(f"User {request.user.username}: {error_message}")
            return JsonResponse({'success': False, 'error': error_message}, status=400)

        # Validate that answer_id is a valid UUID
        try:
            uuid_obj = uuid.UUID(answer_id, version=4)
        except ValueError:
            error_message = 'Invalid answer_id. It must be a valid UUID.'
            logger.warning(f"User {request.user.username}: {error_message}")
            return JsonResponse({'success': False, 'error': error_message}, status=400)

        # Fetch the corresponding question text
        if 0 <= question_index < len(QUESTIONS):
            question_text = QUESTIONS[question_index]
        else:
            error_message = 'Invalid question index.'
            logger.warning(f"User {request.user.username}: {error_message}")
            return JsonResponse({'success': False, 'error': error_message}, status=400)

        # Fetch answer options and responses for the current question
        try:
            current_answers = ANSWERS[question_index]
            response_list = RESPONSES[question_index]
            answer_idx = current_answers.index(answer_text)
            response_text = response_list[answer_idx]
        except (IndexError, ValueError) as e:
            error_message = 'Invalid answer_text provided.'
            logger.error(f"User {request.user.username}: {error_message} Error: {e}")
            return JsonResponse({'success': False, 'error': error_message}, status=400)

        # Prevent duplicate submissions using answer_id
        try:
            with transaction.atomic():
                # Attempt to create the Questionnaire entry
                questionnaire_entry = Questionnaire.objects.create(
                    user=request.user,
                    question=question_text,
                    answer=answer_text,
                    response=response_text,
                    answer_id=answer_id  # Assign the unique answer_id
                )
                logger.info(f"User {request.user.username}: Saved answer_id {answer_id}.")
        except IntegrityError:
            # If a duplicate answer_id exists, respond accordingly
            error_message = 'This answer has already been submitted.'
            logger.warning(f"User {request.user.username}: {error_message}")
            return JsonResponse({'success': False, 'error': error_message}, status=400)

        # Save user message to ChatMessage
        user_message = ChatMessage.objects.create(
            user=request.user,
            message=answer_text,
            is_bot_message=False,
            message_type='user_message',
            question_index=question_index
        )
        logger.debug(f"User {request.user.username}: Saved user message.")

        # Save bot response as ChatMessage
        bot_message = ChatMessage.objects.create(
            user=request.user,
            message=response_text,
            is_bot_message=True,
            message_type='bot_message',
            question_index=question_index
        )
        logger.debug(f"User {request.user.username}: Saved bot message.")

        # Update the QuestionnaireProgress
        progress, created = QuestionnaireProgress.objects.get_or_create(user=request.user)
        if progress.completed:
            error_message = 'You have already completed the questionnaire.'
            logger.warning(f"User {request.user.username}: {error_message}")
            return JsonResponse({'success': False, 'error': error_message}, status=400)

        # Determine the next question index
        next_question_index = question_index + 1

        if next_question_index < len(QUESTIONS):
            # Fetch the next question and its answer options
            next_question_text = QUESTIONS[next_question_index]
            next_answer_options = ANSWERS[next_question_index]

            # Save the next question as a bot message
            next_bot_message = ChatMessage.objects.create(
                user=request.user,
                message=next_question_text,
                is_bot_message=True,
                message_type='question',
                question_index=next_question_index
            )
            logger.debug(f"User {request.user.username}: Sent next question.")

            # Update progress
            progress.last_question_index = next_question_index
            progress.save()
            logger.debug(f"User {request.user.username}: Updated progress to question_index {next_question_index}.")

            return JsonResponse({
                'success': True,
                'response': response_text,
                'next_question_index': next_question_index,
                'question': next_question_text,
                'answer_options': next_answer_options,
                'simulate_typing': True
            })
        else:
            # No more questions; mark the questionnaire as completed
            progress.completed = True
            progress.save()
            logger.info(f"User {request.user.username}: Completed the questionnaire.")

            # Final bot message
            final_bot_message_text = "Thank you for completing the questionnaire! Would you like to talk to a counselor?"
            final_bot_message = ChatMessage.objects.create(
                user=request.user,
                message=final_bot_message_text,
                is_bot_message=True,
                message_type='bot_message',
                question_index=None
            )
            logger.debug(f"User {request.user.username}: Sent final message.")

            return JsonResponse({
                'success': True,
                'response': response_text,
                'end_of_questions': True,
                'final_bot_message': final_bot_message_text,
                'simulate_typing': True
            })

    except json.JSONDecodeError:
        logger.error(f"User {request.user.username}: JSON decoding error.")
        return JsonResponse({'success': False, 'error': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        logger.error(f"User {request.user.username}: Unexpected error: {e}")
        return JsonResponse({'success': False, 'error': 'Failed to process your answer. Please try again.'}, status=500)
@login_required
@csrf_exempt
@require_POST
def handle_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            logger.debug(f"Received message from user '{request.user.username}': {user_message}")

            # Save user message to ChatMessage
            user_chat = ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                is_bot_message=False,
                message_type='user_message'
            )
            logger.info(f"Saved user message: {user_chat}")

            # Initialize or fetch QuestionnaireProgress
            progress, created = QuestionnaireProgress.objects.get_or_create(user=request.user)

            if user_message.lower() == "start":
                if progress.completed:
                    error_message = 'You have already completed the questionnaire.'
                    logger.warning(f"User '{request.user.username}' attempted to start again: {error_message}")
                    bot_message = "You have already completed the questionnaire."
                    ChatMessage.objects.create(
                        user=request.user,  # Bot message
                        message=bot_message,
                        is_bot_message=True,
                        message_type='bot_message'
                    )
                    return JsonResponse({'success': False, 'error': error_message, 'message': bot_message}, status=400)

                # Reset progress if starting anew
                progress.last_question_index = 0
                progress.completed = False
                progress.save()
                logger.info(f"User '{request.user.username}' started the questionnaire.")

                # Fetch the first question
                question_index = progress.last_question_index
                question_text = QUESTIONS[question_index]
                answer_options = ANSWERS[question_index]

                # Save the first question as a bot message
                bot_message = ChatMessage.objects.create(
                    user=request.user,  # Bot message
                    message=question_text,
                    is_bot_message=True,
                    message_type='question',
                    question_index=question_index
                )
                logger.debug(f"Sent first question (index {question_index}): {question_text}")

                return JsonResponse({
                    'success': True,
                    'question_index': question_index,
                    'question': question_text,
                    'answer_options': answer_options,
                    'simulate_typing': True
                })

            elif user_message.lower() == 'not yet':
                bot_message = "No worries, take your time."
                ChatMessage.objects.create(
                    user=request.user,  # Bot message
                    message=bot_message,
                    is_bot_message=True,
                    message_type='bot_message'
                )
                logger.info(f"User '{request.user.username}' chose 'Not Yet'. Sent response: {bot_message}")
                return JsonResponse({'success': True, 'message': bot_message})

            else:
                # Handle other messages or unrecognized commands
                bot_message = "I'm here to help whenever you're ready. Please type 'Start' to begin the questionnaire."
                ChatMessage.objects.create(
                    user=request.user,  # Bot message
                    message=bot_message,
                    is_bot_message=True,
                    message_type='bot_message'
                )
                logger.info(f"Unrecognized message from '{request.user.username}'. Prompted to start.")
                return JsonResponse({'success': False, 'error': 'No action taken.', 'message': bot_message}, status=400)

        except json.JSONDecodeError:
            logger.error(f"JSON decoding error in handle_chat view for user '{request.user.username}'.")
            return JsonResponse({'success': False, 'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error in handle_chat view for user '{request.user.username}': {str(e)}")
            return JsonResponse({'success': False, 'error': 'Failed to process your message. Please try again.'}, status=500)

    logger.warning(f"Invalid request method for handle_chat view by user '{request.user.username}'.")
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
@login_required
@require_POST
def start_questionnaire(request):
    """
    Handles the initiation of the questionnaire.
    Saves the user message and sends the first question.
    """
    try:
        data = json.loads(request.body)
        logger.debug(f"Received data for start_questionnaire: {data}")

        answer_id = data.get('answer_id')

        if not answer_id:
            error_message = "Missing required field: answer_id."
            logger.warning(error_message)
            return JsonResponse({'success': False, 'error': error_message}, status=400)

        # Validate that answer_id is a valid UUID
        try:
            uuid_obj = uuid.UUID(answer_id, version=4)
        except ValueError:
            error_message = 'Invalid answer_id. It must be a valid UUID.'
            logger.warning(error_message)
            return JsonResponse({'success': False, 'error': error_message}, status=400)

        # Save user message
        user_message = ChatMessage.objects.create(
            user=request.user,
            message="Start",
            is_bot_message=False,
            message_type='user_message',
            question_index=None  # Not tied to a specific question
        )
        logger.debug(f"Saved user message: {user_message}")

        # Initialize the questionnaire progress
        progress, created = QuestionnaireProgress.objects.get_or_create(user=request.user)
        if progress.completed:
            error_message = 'You have already completed the questionnaire.'
            logger.warning(error_message)
            return JsonResponse({'success': False, 'error': error_message}, status=400)
        # Reset progress if starting anew
        progress.last_question_index = 0
        progress.completed = False
        progress.save()
        logger.info(f"Initialized questionnaire for user {request.user.username} with answer_id {answer_id}.")

        # Fetch the first question
        question_index = progress.last_question_index
        question_text = QUESTIONS[question_index]
        # Save the first question as a bot message
        bot_message = ChatMessage.objects.create(
            user=request.user,
            message=question_text,
            is_bot_message=True,
            message_type='question',
            question_index=question_index
        )
        logger.debug(f"Sent first question (index {question_index}): {question_text}")

        return JsonResponse({
            'success': True,
            'question_index': question_index,
            'question': question_text,
            'simulate_typing': True
        })

    except json.JSONDecodeError:
        logger.error(f"JSON decoding error in start_questionnaire view for user '{request.user.username}'.")
        return JsonResponse({'success': False, 'error': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in start_questionnaire view for user '{request.user.username}': {str(e)}")
        return JsonResponse({'success': False, 'error': 'Failed to start questionnaire. Please try again.'}, status=500)
@login_required
@csrf_exempt
def final_option_selection(request):
    """
    Handles the final option selections after completing the questionnaire.
    For example, asking if the user wants to talk to a counselor.
    """
    try:
        data = json.loads(request.body)
        logger.debug(f"Received data for final_option_selection: {data}")

        selection = data.get('selection')

        if not selection:
            error_message = "Missing required field: selection."
            logger.warning(error_message)
            return JsonResponse({'success': False, 'error': error_message}, status=400)

        if selection not in ["Yes", "No"]:
            error_message = "Invalid selection. Must be 'Yes' or 'No'."
            logger.warning(error_message)
            return JsonResponse({'success': False, 'error': error_message}, status=400)

        # Save user message to ChatMessage
        user_message = ChatMessage.objects.create(
            user=request.user,
            message=selection,
            is_bot_message=False,
            message_type='user_message',
            question_index=None  # Not tied to a specific question
        )
        logger.debug(f"Saved user message: {user_message}")

        if selection == "Yes":
            # Handle the case where user wants to talk to a counselor
            message = "A counselor will reach out to you shortly."
            logger.info(f"User {request.user.username} opted to talk to a counselor.")
        else:
            # Handle the case where user does not want to talk to a counselor
            message = "Alright, feel free to reach out if you change your mind."
            logger.info(f"User {request.user.username} chose not to talk to a counselor.")

        # Save bot response
        bot_message = ChatMessage.objects.create(
            user=request.user,
            message=message,
            is_bot_message=True,
            message_type='bot_message',
            question_index=None
        )
        logger.debug(f"Sent bot message: {bot_message}")

        return JsonResponse({
            'success': True,
            'message': message,
            'simulate_typing': True
        })

    except json.JSONDecodeError:
        logger.error(f"JSON decoding error in final_option_selection view for user '{request.user.username}'.")
        return JsonResponse({'success': False, 'error': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in final_option_selection view for user '{request.user.username}': {str(e)}")
        return JsonResponse({'success': False, 'error': 'Failed to process your selection. Please try again.'}, status=500)

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        is_bot_message = data.get('is_bot_message')

        if message:
            # Save the message to the database, associating with the user
            ChatMessage.objects.create(
                user=request.user if not is_bot_message else request.user,  # Associate with user
                message=message,
                is_bot_message=is_bot_message,
                created_at=timezone.now()
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No message provided'})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
@csrf_exempt
@login_required
def send_chat_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            is_bot_message = data.get('is_bot_message', False)
            associate_with_user = data.get('associate_with_user', False)  # Custom flag if needed

            if message:
                # Associate all messages with the authenticated user
                user = request.user

                chat_message = ChatMessage.objects.create(
                    user=user,
                    message=message,
                    is_bot_message=is_bot_message,
                    message_type='bot_message' if is_bot_message else 'user_message'
                )
                logger.info(f"Saved {'bot' if is_bot_message else 'user'} message: {chat_message}")

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'No message provided'}, status=400)
        except json.JSONDecodeError:
            logger.error("JSON decoding error in send_chat_message view.")
            return JsonResponse({'success': False, 'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error in send_chat_message view: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Failed to save the message.'}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

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
def is_auto_accept_enabled():
    return SystemSetting.get_setting('auto_accept_enabled', 'false') == 'true'

def is_auto_reject_enabled():
    return SystemSetting.get_setting('auto_reject_enabled', 'false') == 'true'

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            message = ''
            try:
                # Verify if the user details are in the EnrollmentMasterlist
                EnrollmentMasterlist.objects.get(
                    student_id=user.student_id.strip(),
                    full_name=user.full_name.strip(),
                    academic_year_level=user.academic_year_level.strip()
                )

                if is_auto_accept_enabled():
                    # Auto-accept enabled: set user as verified and active
                    user.is_active = True
                    user.is_verified = True
                    user.verification_status = 'verified'
                    message = 'Your account has been automatically verified based on ITRC records.'

                elif is_auto_reject_enabled():
                    # Auto-reject enabled: set user as inactive and not verified
                    user.is_active = False
                    user.is_verified = False
                    user.verification_status = 'rejected'
                    message = 'The ITRC has automatically rejected your registration. Please contact support if you have questions.'

                else:
                    # Disable automatic: set user as active but not verified
                    user.is_active = True
                    user.is_verified = False
                    user.verification_status = 'pending'
                    message = 'Your registration is pending manual verification.'

            except EnrollmentMasterlist.DoesNotExist:
                # User not found in master list, proceed with pending status
                user.is_active = True
                user.is_verified = False
                user.verification_status = 'pending'
                message = 'Your registration is pending manual verification.'

            user.save()

            # Create a verification request if manual verification is needed
            if user.verification_status == 'pending':
                VerificationRequest.objects.create(user=user)

            # Log the registration action in the audit log
            AuditLog.objects.create(
                user=user,
                action='register',
                details=f"User {user.username} registered at {timezone.now()} with verification status '{user.verification_status}'."
            )

            return JsonResponse({
                'success': True,
                'message': message,
                'redirect_url': '/login/'
            })

        # Return errors if the form is not valid
        errors = form.errors.get_json_data()
        return JsonResponse({'success': False, 'error_message': errors}, status=400)
    
    # Display the registration form
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
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.check_password(password):
                    if user.is_active:
                        # User is active, proceed to login
                        login(request, user)
                        handle_session_tracking(request, user)
                        return JsonResponse({'success': True, 'message': 'Login successful!', 'redirect_url': '/'})
                    else:
                        # User account is inactive, check verification status
                        if user.verification_status == 'pending':
                            user = process_pending_user(user)  # Recheck auto-accept/reject conditions
                            if user.is_active:
                                login(request, user)
                                handle_session_tracking(request, user)
                                return JsonResponse({'success': True, 'message': 'Login successful!', 'redirect_url': '/'})
                            else:
                                # User remains inactive, return appropriate error
                                error_message = get_pending_account_message(user)
                                return JsonResponse({'success': False, 'error_message': error_message}, status=400)
                        elif user.verification_status == 'rejected':
                            # Account has been rejected
                            error_message = get_rejected_account_message()
                            return JsonResponse({'success': False, 'error_message': error_message}, status=400)
                        else:
                            # Account is inactive for another reason
                            error_message = get_inactive_account_message()
                            return JsonResponse({'success': False, 'error_message': error_message}, status=400)
                else:
                    form.add_error(None, "Invalid login credentials")
            else:
                form.add_error(None, "Invalid login credentials")
        
        # If form is invalid or other errors occur
        errors = form.errors.get_json_data()
        return JsonResponse({'success': False, 'error_message': errors})

    form = CustomAuthenticationForm()
    return render(request, 'base.html', {'login_form': form, 'show_login_modal': True})

def process_pending_user(user):
    try:
        # Verify if the user details are in the EnrollmentMasterlist
        EnrollmentMasterlist.objects.get(
            student_id=user.student_id.strip(),
            full_name=user.full_name.strip(),
            academic_year_level=user.academic_year_level.strip()
        )

        if is_auto_accept_enabled():
            # Auto-activate and verify the user
            user.is_active = True
            user.is_verified = True
            user.verification_status = 'verified'
            user.save()

            # Remove any existing verification requests
            VerificationRequest.objects.filter(user=user).delete()

            # Send notification to the user
            Notification_System.objects.create(
                user=user,
                notification_type='success',
                message='Your account has been automatically verified by the ITRC staff.',
                link=reverse('itrc_dashboard')  # Adjust as needed
            )

        else:
            # Auto-accept not enabled, user remains pending
            pass

    except EnrollmentMasterlist.DoesNotExist:
        # User details not found in EnrollmentMasterlist
        if is_auto_reject_enabled():
            # Auto-reject the user
            user.is_active = True
            user.is_verified = False
            user.verification_status = 'rejected'
            user.save()

            # Remove any existing verification requests
            VerificationRequest.objects.filter(user=user).delete()

            # Send notification to the user
            Notification_System.objects.create(
                user=user,
                notification_type='warning',
                message='Your account has been automatically rejected by the ITRC staff.',
                link=reverse('contact_support')  # Adjust as needed
            )
        else:
            # Auto-reject not enabled, user remains pending
            pass
    return user

def handle_session_tracking(request, user):
    # Handle session tracking
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    try:
        session = Session.objects.get(session_key=session_key)
        expire_date = session.expire_date
    except Session.DoesNotExist:
        expire_date = timezone.now() + timezone.timedelta(days=1)  # Default expiration

    # Create a UserSession entry
    UserSession.objects.create(
        user=user,
        session_key=session_key,
        created_at=timezone.now(),
        expire_date=expire_date
    )

def get_pending_account_message(user):
    if is_auto_accept_enabled() or is_auto_reject_enabled():
        # Auto accept/reject is enabled but user remains pending
        message = {
            '__all__': [
                {
                    'message': 'Your account is pending verification.',
                    'code': 'pending_verification'
                }
            ]
        }
    else:
        # Auto accept/reject is not enabled
        message = {
            '__all__': [
                {
                    'message': 'Your account is pending manual verification.',
                    'code': 'inactive'
                }
            ]
        }
    return message

def get_rejected_account_message():
    message = {
        '__all__': [
            {
                'message': 'Your account has been rejected.',
                'code': 'rejected'
            }
        ]
    }
    return message

def get_inactive_account_message():
    message = {
        '__all__': [
            {
                'message': 'Your account is inactive.',
                'code': 'inactive'
            }
        ]
    }
    return message



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
            title = data.get('title', '').strip()
            description = data.get('description', '').strip()
            emotion = data.get('emotion', '').strip()
        else:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            emotion = request.POST.get('emotion', '').strip()
        
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

        # Notification Logic
        # Define thresholds for emotions to trigger notifications
        emotion_thresholds = {
            'anger': 70,
            'disgust': 70,
            'fear': 70,
            'happiness': 70,
            'sadness': 70,
            'surprise': 70,
            'neutral': 70,
        }

        # Check if any emotion exceeds the threshold
        for emotion_label, threshold in emotion_thresholds.items():
            if emotion_percentages[emotion_label] >= threshold:
                # Create a concise, user-friendly notification message
                emotion_name = emotion_label.capitalize()
                message = (
                    f"{request.user.username} posted a status with high {emotion_name} ({emotion_percentages[emotion_label]}%). "
                    "You may want to check in."
                )

                # Create a notification entry for all counselors
                counselors = CustomUser.objects.filter(is_counselor=True)
                for counselor in counselors:
                    NotificationCounselor.objects.create(
                        user=counselor,
                        message=message,
                        link=reverse('status_detail', args=[status.id]),
                        is_read=False,
                        status=status  # Associate the notification with the status
                    )
                break  # Only notify once per status

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
def load_emojis(request):
    category = request.GET.get('category', None)
    search_query = request.GET.get('search', "").strip()
    page = request.GET.get('page', 1)
    per_page = 50  # Number of emojis per page

    logger.debug(f"Loading emojis with category: '{category}', search_query: '{search_query}', page: {page}")

    try:
        emojis = Emoji.objects.all()

        if category:
            emojis = emojis.filter(group__iexact=category)
            logger.debug(f"Filtered by category '{category}', count: {emojis.count()}")

        if search_query:
            emojis = emojis.filter(name__icontains=search_query)
            logger.debug(f"Filtered by search_query '{search_query}', count: {emojis.count()}")

        # Order emojis by group, sub_group, and name
        emojis = emojis.order_by('group', 'sub_group', 'name')

        paginator = Paginator(emojis, per_page)
        try:
            emojis_page = paginator.page(page)
        except PageNotAnInteger:
            logger.warning(f"Page '{page}' is not an integer. Serving page 1.")
            emojis_page = paginator.page(1)
        except EmptyPage:
            logger.warning(f"Page '{page}' is out of range. Serving last page.")
            emojis_page = paginator.page(paginator.num_pages)

        emojis_data = [
            {'emoji': emoji.emoji, 'name': emoji.name}
            for emoji in emojis_page.object_list
        ]

        has_more = emojis_page.has_next()

        logger.debug(f"Emojis returned: {len(emojis_data)}, has_more: {has_more}")

        return JsonResponse({'emojis': emojis_data, 'has_more': has_more})

    except Exception as e:
        logger.error(f"Error in load_emojis view: {e}")
        return JsonResponse({'emojis': [], 'has_more': False, 'error': 'An error occurred while fetching emojis.'}, status=500)

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
        user = request.user
        session_key = request.session.session_key

        # Create an AuditLog entry for logout
        AuditLog.objects.create(
            user=user,
            action='logout',
            details=f"User {user.username} logged out at {timezone.now()}."
        )

        # Update the UserSession entry with session_end
        try:
            user_session = UserSession.objects.get(user=user, session_key=session_key, session_end__isnull=True)
            user_session.session_end = timezone.now()
            user_session.save()
        except UserSession.DoesNotExist:
            # Handle cases where the session is not found or already ended
            pass

        logout(request)
        return JsonResponse({'success': True, 'message': 'Logout successful!', 'redirect_url': '/'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)