# admin_tools/views.py

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.views.decorators.http import require_http_methods, require_POST
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from django.db.models import Count, Case, When, Value, DurationField
import matplotlib
matplotlib.use('Agg')  # Must be set before importing pyplot
from reportlab.lib.pagesizes import A4, landscape  
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
)
import numpy as np
import base64 
import matplotlib.pyplot as plt
import io
from django.utils.timezone import now
from django.core.files.base import ContentFile
import csv
from django.urls import reverse
import threading
import seaborn as sns
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from main.models import (
    ContactUs,
    Status,
    CustomUser,
    Reply,
    Feedback,
    Referral,
    ProfanityWord,
    Questionnaire,
    TextAnalysis,
)
import torch
from django.contrib import messages
import pandas as pd
import plotly.express as px
import plotly.io as pio
from wordcloud import WordCloud
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
import zipfile
from io import BytesIO
from .forms import DatasetUploadForm
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
from main.models import Dataset, PerformanceResult
from datetime import timedelta
from datetime import datetime
import os
from django.conf import settings
from main.models import NLTKResource
import logging
# admin_tools/views.py

# After other imports
logger = logging.getLogger(__name__)

# Define the directory for NLTK data inside the project
nltk_data_path = os.path.join(settings.BASE_DIR, 'nltk_data')

# Ensure the directory exists
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

# Set the NLTK_DATA environment variable to this directory
os.environ['NLTK_DATA'] = nltk_data_path

# Suppress unnecessary logs from NLTK downloads
nltk_logger = logging.getLogger('nltk')
nltk_logger.setLevel(logging.CRITICAL)

def is_counselor(user):
    return user.is_authenticated and user.is_counselor

@login_required
@require_GET
def get_progress(request, dataset_id):
    """
    API endpoint to retrieve the progress of a dataset.
    """
    dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)
    return JsonResponse({'progress': dataset.progress})

@login_required
@user_passes_test(is_counselor)
def performance_dashboard(request):
    if not request.user.is_counselor:
        return redirect('admin_login')

    dataset_id = request.GET.get('dataset_id')
    performance_result = None
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)
    page_size = 10
    page_obj = None  # Initialize page_obj to ensure it has a value

    if request.method == 'POST':
        # Handle dataset upload
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.user = request.user
            dataset.status = 'processing'
            dataset.name = os.path.splitext(os.path.basename(dataset.csv_file.name))[0]
            dataset.save()

            # Start dataset processing in background
            threading.Thread(target=process_dataset, args=(dataset.id,)).start()

            messages.success(request, 'Dataset uploaded and processing started.')
            return redirect(f'{reverse("performance_dashboard")}?dataset_id={dataset.id}')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = DatasetUploadForm()

    if dataset_id:
        # Fetch performance results for a specific dataset
        dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)
        if dataset.status == 'completed':
            performance_result = PerformanceResult.objects.get(dataset=dataset)
            
            text_analyses = TextAnalysis.objects.filter(dataset=dataset)
            if search_query:
                text_analyses = text_analyses.filter(
                    Q(analysis_data__text__icontains=search_query) |
                    Q(analysis_data__actual_label__icontains=search_query) |
                    Q(analysis_data__predicted_label__icontains=search_query)
                )

            paginator = Paginator(text_analyses, page_size)
            page_obj = paginator.get_page(page_number)
        elif dataset.status == 'processing':
            # Handle processing status
            pass
        elif dataset.status == 'failed':
            # Handle failed status
            messages.error(request, f'Dataset processing failed: {dataset.error_log}')
        else:
            # Handle any other statuses if applicable
            pass
    else:
        # Load the latest performance result if no dataset is specified
        latest_performance = PerformanceResult.objects.filter(
    dataset__status='completed', dataset__user=request.user
).order_by('-created_at').first()
        if latest_performance:
            performance_result = latest_performance
            dataset_id = latest_performance.dataset.id
            text_analyses = TextAnalysis.objects.filter(dataset=latest_performance.dataset)
            paginator = Paginator(text_analyses, page_size)
            page_obj = paginator.get_page(page_number)

    # The context includes page_obj regardless of the dataset status
    context = {
        'form': form,
        'dataset_id': dataset_id,
        'performance_result': performance_result,
        'page_obj': page_obj,  # Will be None if not assigned above
        'search_query': search_query,
    }
    return render(request, 'admin_tools/performance_dashboard.html', context)

def process_dataset(dataset_id):
    """
    Function to process the dataset and update progress.
    Runs in a separate thread.
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        dataset.status = 'processing'
        dataset.progress = {'current_task': 'Reading CSV', 'percentage': 10}
        dataset.save()

        # Read CSV
        df = pd.read_csv(dataset.csv_file)
        dataset.progress = {'current_task': 'Splitting Data', 'percentage': 20}
        dataset.save()

        # Ensure 'Label' column is treated as string
        df['Label'] = df['Label'].astype(str)

        X = df['Text']
        y = df['Label']

        # Check for null values
        if X.isnull().any() or y.isnull().any():
            dataset.progress = {'current_task': 'Error: Null values found', 'percentage': 100}
            dataset.status = 'failed'
            dataset.error_log = 'Null values found in the dataset.'
            dataset.save()
            return

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        dataset.progress = {'current_task': 'Loading Model', 'percentage': 30}
        dataset.save()

        # Load model and tokenizer
        model_name = 'j-hartmann/emotion-english-distilroberta-base'
        token = os.getenv('HUGGINGFACE_HUB_TOKEN')  # Ensure this is set if the model is private
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, use_auth_token=token)
        model.eval()
        dataset.progress = {'current_task': 'Making Predictions', 'percentage': 40}
        dataset.save()

        # Make predictions and update progress
        y_pred = []
        total = len(X_test)
        for idx, text in X_test.items():
            if isinstance(text, str):
                inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
                with torch.no_grad():
                    outputs = model(**inputs)
                    logits = outputs.logits
                    scores = logits.squeeze().tolist()

                    # Use the emotion mapping provided to get the dominant emotion
                    emotions = {
                        'anger': scores[0],
                        'disgust': scores[1],
                        'fear': scores[2],
                        'happiness': scores[3],
                        'neutral': scores[4],
                        'sadness': scores[5],
                        'surprise': scores[6],
                    }

                    # Get the emotion with the highest score
                    predicted_label = max(emotions, key=emotions.get)
                y_pred.append(predicted_label)
            else:
                y_pred.append(None)

            # Update progress
            current_percentage = 40 + int((len(y_pred) / total) * 60)
            dataset.progress = {
                'current_task': 'Making Predictions',
                'percentage': min(current_percentage, 99),
            }
            dataset.save()

        # Clean predictions
        valid_indices = [i for i, pred in enumerate(y_pred) if pred is not None]
        y_test_clean = y_test.iloc[valid_indices]
        y_pred_clean = [y_pred[i] for i in valid_indices]

        dataset.progress = {'current_task': 'Calculating Metrics', 'percentage': 90}
        dataset.save()

        # Calculate metrics
        accuracy = accuracy_score(y_test_clean, y_pred_clean)
        precision = precision_score(y_test_clean, y_pred_clean, average='weighted', zero_division=0)
        recall = recall_score(y_test_clean, y_pred_clean, average='weighted', zero_division=0)
        f1 = f1_score(y_test_clean, y_pred_clean, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test_clean, y_pred_clean)

        # Generate classification report as HTML and CSV
        class_report = classification_report(y_test_clean, y_pred_clean, output_dict=True)
        report_df = pd.DataFrame(class_report).transpose().round(2)
        report_html = report_df.to_html(
            classes='pilarease-admin-classification-report-table', border=0
        )
        report_csv = report_df.to_csv(index=True)
        report_csv_base64 = base64.b64encode(report_csv.encode('utf-8')).decode('utf-8')

        # Plot confusion matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('Actual Labels')
        plt.xlabel('Predicted Labels')
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plot_url = base64.b64encode(image_png).decode('utf-8')
        plt.close()

        # Add 'Predicted Label' to the original DataFrame
        df['Predicted Label'] = pd.NA  # Initialize with NA
        df.loc[y_test_clean.index, 'Predicted Label'] = y_pred_clean

        # Save individual analyses to the database using JSONField
        for idx, actual_label, predicted_label in zip(y_test_clean.index, y_test_clean, y_pred_clean):
            text = df.loc[idx, 'Text']
            analysis_data = {
                "text": text,
                "actual_label": actual_label,
                "predicted_label": predicted_label,
            }
            analysis = TextAnalysis(
                dataset=dataset,
                analysis_data=analysis_data,  # Save all data in JSONField
            )
            analysis.save()

        # Save the processed CSV to a new file in memory
        processed_buffer = io.StringIO()
        df.to_csv(processed_buffer, index=False)
        processed_csv_content = processed_buffer.getvalue()
        processed_buffer.close()

        # Save the processed CSV file to PerformanceResult
        performance_result = PerformanceResult.objects.create(
            dataset=dataset,
            accuracy=round(accuracy * 100, 2),
            precision=round(precision * 100, 2),
            recall=round(recall * 100, 2),
            f1_score=round(f1 * 100, 2),
            confusion_matrix_image=plot_url,
            classification_report_html=report_html,
            classification_report_csv=report_csv_base64,
        )

        # Save the processed CSV file
        performance_result.processed_csv_file.save(
            f"processed_dataset_{dataset_id}.csv",
            ContentFile(processed_csv_content.encode('utf-8')),
            save=True,
        )

        # Final progress update
        dataset.progress = {
            'current_task': 'Completed',
            'percentage': 100,
            'result_id': performance_result.id,
        }
        dataset.status = 'completed'
        dataset.save()

    except Exception as e:
        logger.exception(f"Error processing dataset {dataset_id}: {e}")
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            dataset.status = 'failed'
            dataset.progress = {'current_task': f'Error: {str(e)}', 'percentage': 100}
            dataset.error_log = str(e)
            dataset.save()
        except Dataset.DoesNotExist:
            logger.error(f"Dataset {dataset_id} does not exist.")

def performance_dashboard_result(request):
    """
    View to display the performance results and the processed dataset.
    """
    dataset_id = request.GET.get('dataset_id')
    if not dataset_id:
        messages.error(request, "No dataset specified.")
        return redirect('performance_dashboard')

    dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)

    try:
        # Get all the text analyses for the dataset
        text_analyses = TextAnalysis.objects.filter(dataset=dataset)

        # Pagination
        paginator = Paginator(text_analyses, 10)  # Show 10 entries per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except TextAnalysis.DoesNotExist:
        messages.error(request, "Performance results not found.")
        return redirect('performance_dashboard')

    context = {
        'page_obj': page_obj,  # Pass paginated results to the template
    }
    return render(request, 'admin_tools/performance_dashboard_result.html', context)

@user_passes_test(is_counselor)
@login_required
def get_user_questionnaire(request, user_id):
    """
    Fetch all questionnaire responses and basic profile details for a specific user.
    Only accessible by counselors.
    """
    # Ensure the user is a student
    user = get_object_or_404(CustomUser, id=user_id, is_counselor=False)
    
    # Fetch questionnaire responses
    questionnaires = Questionnaire.objects.filter(user=user).order_by('timestamp')
    
    # Serialize questionnaire data
    questionnaire_data = []
    for q in questionnaires:
        questionnaire_data.append({
            'question': q.question,
            'answer': q.answer,
            'response': q.response,
            'timestamp': q.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        })
    
    # Serialize user profile data
    profile_data = {
        'student_id': user.student_id,
        'full_name': user.full_name,
        'academic_year_level': user.academic_year_level,
        'contact_number': user.contact_number,
        'email': user.email,
        'bio': user.profile.bio or 'No bio available.',
        'avatar_url': user.profile.avatar.url if user.profile.avatar else '',  # Empty string if no avatar
    }
    
    return JsonResponse({
        'questionnaires': questionnaire_data,
        'profile': profile_data,
    })
# Function to save NLTK resource download status to the database
def save_nltk_resource(resource_name):
    resource, created = NLTKResource.objects.get_or_create(
        name=resource_name,
        defaults={'is_downloaded': True, 'download_date': timezone.now()}
    )
    if not created:
        resource.is_downloaded = True
        resource.download_date = timezone.now()
        resource.save()

# Silent download function for NLTK resources if they are missing
def silent_nltk_download(resource_name):
    try:
        # Check if the resource exists in the database
        resource = NLTKResource.objects.filter(name=resource_name, is_downloaded=True).first()
        if resource:
            print(f"{resource_name} already downloaded.")
            return
        
        # Check if the resource is already downloaded in nltk_data_path
        if resource_name == 'punkt':
            nltk.data.find('tokenizers/punkt/english.pickle')
        elif resource_name == 'stopwords':
            nltk.data.find('corpora/stopwords.zip')
        
        # Save the resource to the database as downloaded
        save_nltk_resource(resource_name)
        
    except LookupError:
        # If the resource is not found, download it silently
        print(f"Downloading {resource_name}...")
        nltk.download(resource_name, download_dir=nltk_data_path)
        
        # Save the download status to the database
        save_nltk_resource(resource_name)

@login_required
def manage_users_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        users = CustomUser.objects.filter(
            Q(username__icontains=search_query) |
            Q(student_id__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(academic_year_level__icontains=search_query) |
            Q(contact_number__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    else:
        users = CustomUser.objects.all()

    # Optional: Order by date joined descending
    users = users.order_by('-date_joined')

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
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False  # Soft delete
    user.block_reason = 'Deleted by admin.'
    user.block_duration = None
    # user.blocked_at = timezone.now()  # If 'blocked_at' field exists
    user.save()
    messages.success(request, f'User "{user.username}" has been deactivated successfully.')
    return redirect('manage_users')

@login_required
def block_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            reason = data.get('reason')
            duration = data.get('duration')

            # Validate input
            if not all([user_id, reason, duration]):
                return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

            user = CustomUser.objects.get(id=user_id)

            # Update user status
            user.is_active = False
            user.block_reason = reason
            user.block_duration = duration
            # Note: The model does not have a 'blocked_at' field
            # If you wish to track when the user was blocked, consider adding a 'blocked_at' DateTimeField
            # user.blocked_at = timezone.now()
            user.save()

            return JsonResponse({'success': True, 'message': 'User has been blocked successfully.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)



# Ensure required NLTK data is available silently
silent_nltk_download('punkt')
silent_nltk_download('stopwords')

# Now you can use NLTK in your views like this
def my_nltk_view(request):
    text = request.GET.get('text', '')
    words = nltk.word_tokenize(text.lower())
    stop_words = set(nltk.corpus.stopwords.words('english'))
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

    return JsonResponse({'filtered_words': filtered_words})
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
        replies = Reply.objects.filter(text__icontains=search_query).select_related('user', 'user__profile', 'status')
    else:
        replies = Reply.objects.all().select_related('user', 'user__profile', 'status')

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
            'last_sent': timesince(reply.created_at, current_time),
            'avatar_url': reply.user.profile.avatar.url if reply.user.profile.avatar else 'static/images/placeholder.png',
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
        ).select_related('user', 'user__profile')
    else:
        statuses = Status.objects.filter(
            Q(title__icontains=search_query) |
            Q(plain_description__icontains=search_query),
            emotion=category
        ).select_related('user', 'user__profile')

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

    # Testimonials (approved feedbacks, including excluded)
    testimonial_search_query = request.GET.get('testimonial_search', '')
    testimonials_queryset = Feedback.objects.filter(is_approved=True)  # Removed is_excluded=False
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
def exclude_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Feedback, id=testimonial_id, is_excluded=False)
    testimonial.is_excluded = True
    testimonial.save()
    return JsonResponse({'success': True})

@login_required
def unexclude_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Feedback, id=testimonial_id, is_excluded=True)
    testimonial.is_excluded = False
    testimonial.save()
    return JsonResponse({'success': True})

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

# ==============================
# Referral Management Views
# ==============================

@login_required
@user_passes_test(is_counselor)
def manage_referrals_view(request):
    referrals = Referral.objects.select_related('status', 'referred_by').all().order_by('-created_at')
    profanity_words = ProfanityWord.objects.first()
    profanities = profanity_words.word_list if profanity_words else []
    context = {
        'referrals': referrals,
        'profanities': profanities,
    }
    return render(request, 'admin_tools/referral.html', context)

@login_required
def profanity_list(request):
    # Ensure only counselors can access the profanity list
    if not request.user.is_counselor:
        return redirect('admin_login')

    # Retrieve the ProfanityWord object
    profanity_obj = ProfanityWord.objects.first()
    if profanity_obj:
        word_list = profanity_obj.word_list
    else:
        word_list = []

    # Apply search filter
    search_query = request.GET.get('search', '').strip().lower()
    if search_query:
        filtered_words = [word for word in word_list if search_query in word.lower()]
    else:
        filtered_words = word_list

    # Implement pagination
    paginator = Paginator(filtered_words, 10)  # Show 10 words per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate the starting index for numbering
    start_index = (page_obj.number - 1) * paginator.per_page

    context = {
        'profanities': page_obj,
        'search_query': search_query,
        'start_index': start_index,
    }
    return render(request, 'admin_tools/profanity_list.html', context)

@login_required
@user_passes_test(is_counselor)
def referral_view(request):
    """
    Handles the Referral Management page with search and pagination.
    """
    search_query = request.GET.get('search', '').strip()
    category = request.GET.get('category', 'all').strip().lower()
    page_number = request.GET.get('page', 1)

    # Fetch referrals, optimizing queries with select_related
    referrals = Referral.objects.select_related('referred_by', 'status__user').all()

    # Apply search filters if a search query is provided
    if search_query:
        referrals = referrals.filter(
            Q(referral_reason__icontains=search_query) |
            Q(referred_by__username__icontains=search_query) |
            Q(status__title__icontains=search_query)
        )

    # Apply category filter if not 'all'
    if category and category != 'all':
        referrals = referrals.filter(status__emotion__iexact=category)

    # Paginate the referrals, 10 per page
    paginator = Paginator(referrals.order_by('-created_at'), 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'referrals': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
        'category': category,
        'profanities': ProfanityWord.objects.first().word_list if ProfanityWord.objects.exists() else [],
    }

    return render(request, 'admin_tools/referral.html', context)

@require_http_methods(["GET", "POST"])
@login_required
@user_passes_test(is_counselor)
def referral_detail_view(request, referral_id):
    """
    Handles fetching and updating referral details via AJAX.
    """
    try:
        referral = Referral.objects.select_related('referred_by', 'status').get(id=referral_id)
    except Referral.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Referral not found.'}, status=404)

    if request.method == "GET":
        # Return referral details as JSON
        data = {
            'id': referral.id,
            'status_user_avatar_url': referral.status.user.profile.avatar.url if referral.status.user.profile.avatar else '',
            'status_user_username': referral.status.user.username,
            'highlighted_title': referral.highlighted_title or '',
            'highlighted_description': referral.highlighted_description or '',
            'referral_reason': referral.referral_reason,
            'other_reason': referral.other_reason or '',
            'posted_by_username': referral.status.user.username,
            'referred_by_username': referral.referred_by.username,
        }
        return JsonResponse(data)

    elif request.method == "POST":
        # Handle updating referral details
        try:
            data = json.loads(request.body)
            highlighted_title = data.get('highlighted_title', '').strip()
            highlighted_description = data.get('highlighted_description', '').strip()

            if not highlighted_title or not highlighted_description:
                return JsonResponse({'status': 'error', 'message': 'Fields cannot be empty.'}, status=400)

            referral.highlighted_title = highlighted_title
            referral.highlighted_description = highlighted_description
            referral.save()

            return JsonResponse({'status': 'success', 'message': 'Referral updated successfully.'})

        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')


@login_required
@user_passes_test(is_counselor)
@require_http_methods(["GET", "POST"])
def get_referral_details(request, referral_id):
    referral = get_object_or_404(Referral, id=referral_id)
    
    if request.method == "GET":
        data = {
            "id": referral.id,
            "highlighted_title": referral.highlighted_title,
            "highlighted_description": referral.highlighted_description,
            "referral_reason": referral.referral_reason,
            "other_reason": referral.other_reason,
            "user": {
                "username": referral.referred_by.username,
                "avatar_url": referral.referred_by.profile.avatar.url if referral.referred_by.profile.avatar else "/static/default_avatar.png",
            },
            "status": referral.status.title if referral.status else "N/A",
        }
        return JsonResponse(data)
    
    elif request.method == "POST":
        try:
            payload = json.loads(request.body)
            highlighted_title = payload.get("highlighted_title", "").strip()
            highlighted_description = payload.get("highlighted_description", "").strip()
            
            if not highlighted_title or not highlighted_description:
                return HttpResponseBadRequest("Title and Description cannot be empty.")
            
            referral.highlighted_title = highlighted_title
            referral.highlighted_description = highlighted_description
            referral.save()
            
            return JsonResponse({"status": "success", "message": "Referral updated successfully."})
        
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON.")

@login_required
def referral_management_view(request):
    """
    Renders the referral management page with all referrals.
    """
    # Fetch all referrals, optionally filtering based on permissions
    referrals = Referral.objects.select_related('referred_by', 'status').all().order_by('-created_at')
    
    context = {
        'referrals': referrals
    }
    
    return render(request, 'admin_tools/referral.html', context)

# ==============================
# Profanity Management Views
# ==============================

@login_required
@user_passes_test(is_counselor)
def manage_profanities_view(request):
    profanity_words = ProfanityWord.objects.first()
    if not profanity_words:
        profanity_words = ProfanityWord.objects.create(word_list=[])
    context = {
        'profanities': profanity_words.word_list,
    }
    return render(request, 'admin_tools/profanity_list.html', context)
@require_http_methods(["POST"])
@login_required
@user_passes_test(is_counselor)
def add_profanity(request):
    # Ensure only counselors can add profanity
    if not request.user.is_counselor:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    words = data.get('words', [])
    errors = []

    # Get or create the ProfanityWord object
    profanity_obj, created = ProfanityWord.objects.get_or_create(id=1, defaults={'word_list': []})

    for word in words:
        word = word.strip().lower()
        if word:
            if word in profanity_obj.word_list:
                errors.append(f'"{word}" already exists.')
            else:
                profanity_obj.word_list.append(word)
        else:
            errors.append('Invalid word.')

    if errors:
        return JsonResponse({'success': False, 'error': ' '.join(errors)})

    profanity_obj.save()
    return JsonResponse({'success': True})

@require_http_methods(["POST"])
@login_required
@user_passes_test(is_counselor)
def delete_profanity(request):
    # Ensure only counselors can delete profanity
    if not request.user.is_counselor:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    word = data.get('word', '').strip().lower()

    if word:
        # Get the ProfanityWord object
        profanity_obj = ProfanityWord.objects.first()
        if profanity_obj and word in profanity_obj.word_list:
            profanity_obj.word_list.remove(word)
            profanity_obj.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Word not found.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid word.'})
# ==============================
# API Endpoints for Referrals
# ==============================

@login_required
@user_passes_test(is_counselor)
def referrals_api(request):
    if request.method == "GET":
        referrals = Referral.objects.select_related('status', 'referred_by__profile').all()
        referrals_data = []
        for referral in referrals:
            referrals_data.append({
                "id": referral.id,
                "highlighted_title": referral.highlighted_title,
                "highlighted_description": referral.highlighted_description,
                "referral_reason": referral.referral_reason,
                "other_reason": referral.other_reason,
                "user": {
                    "username": referral.referred_by.username,
                    "avatar_url": referral.referred_by.profile.avatar.url if referral.referred_by.profile.avatar else "/static/default_avatar.png",
                },
                "status": referral.status.title if referral.status else "N/A",
            })
        return JsonResponse({"referrals": referrals_data})
    else:
        return HttpResponseBadRequest("Only GET method is allowed.")

@login_required
@user_passes_test(is_counselor)
def add_profanity_api(request):
    """
    Handles adding a new profanity word via AJAX.
    """
    try:
        data = json.loads(request.body)
        word = data.get('word', '').strip().lower()
        if not word:
            return JsonResponse({'status': 'error', 'message': 'No word provided.'}, status=400)
        
        # Retrieve or create the ProfanityWord instance
        profanity_word_obj, created = ProfanityWord.objects.get_or_create(id=1, defaults={'word_list': []})
        if word in profanity_word_obj.word_list:
            return JsonResponse({'status': 'error', 'message': 'Word already exists.'}, status=400)
        
        # Add the word to the word_list
        profanity_word_obj.word_list.append(word)
        profanity_word_obj.save()
        
        return JsonResponse({'status': 'success', 'message': 'Profanity word added successfully.'})
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

@login_required
@user_passes_test(is_counselor)
@require_http_methods(["POST"])
def delete_profanity_api(request):
    """
    Handles deleting a profanity word via AJAX.
    """
    try:
        data = json.loads(request.body)
        word = data.get('word', '').strip().lower()
        if not word:
            return JsonResponse({'status': 'error', 'message': 'No word provided.'}, status=400)
        
        # Retrieve the ProfanityWord instance
        profanity_word_obj = ProfanityWord.objects.first()
        if not profanity_word_obj or word not in profanity_word_obj.word_list:
            return JsonResponse({'status': 'error', 'message': 'Word not found.'}, status=404)
        
        # Remove the word from the word_list
        profanity_word_obj.word_list.remove(word)
        profanity_word_obj.save()
        
        return JsonResponse({'status': 'success', 'message': 'Profanity word deleted successfully.'})
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

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
def chat_view(request):
    # Fetch users who are not counselors
    users = CustomUser.objects.filter(is_counselor=False)
    return render(request, 'admin_tools/chat.html', {'users': users})
@login_required
@user_passes_test(is_counselor)
def download_statistics_report(request):
    """
    Generates a detailed PDF report with data from all visualizations in the statistics view,
    including key metrics, table data, and embedded chart images.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="statistics_report_{now().strftime("%Y-%m-%d")}.pdf"'
    
    # Set up PDF document with landscape orientation
    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Centered', alignment=1))

    # Title
    elements.append(Paragraph("Statistics Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated on {now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Centered']))
    elements.append(Spacer(1, 24))

    # Retrieve and process Status data
    statuses = Status.objects.all().values()
    df_statuses = pd.DataFrame(statuses)
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

    # Calculate positive, neutral, and negative percentages
    if df_statuses.empty:
        positive_percent = neutral_percent = negative_percent = 0
    else:
        positive_percent = df_statuses['happiness_percentage'].mean()
        neutral_percent = df_statuses['neutral_percentage'].mean()
        negative_percent = (
            df_statuses['anger_percentage'].mean() +
            df_statuses['fear_percentage'].mean() +
            df_statuses['sadness_percentage'].mean()
        )

    # Total students
    total_students = CustomUser.objects.filter(is_active=True).count()
    emotion_percentages = df_statuses[emotion_percentage_columns].mean().round(2).tolist()
    pie_labels = [label.replace('_percentage', '').capitalize() for label in emotion_percentage_columns]
    pie_data = emotion_percentages

    # Section 1: Summary Metrics Table
    elements.append(Paragraph("Summary Metrics", styles['Heading2']))
    summary_data = [
        ['Metric', 'Value'],
        ['Positive Percentage', f"{positive_percent:.2f}%"],
        ['Neutral Percentage', f"{neutral_percent:.2f}%"],
        ['Negative Percentage', f"{negative_percent:.2f}%"],
        ['Total Students', total_students],
    ]
    summary_table = Table(summary_data, hAlign='LEFT', colWidths=[200, 200])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 24))

    # Section 2: Emotion Percentages Table
    elements.append(Paragraph("Emotion Percentages", styles['Heading2']))
    emotion_data = [['Emotion', 'Average Percentage']]
    emotion_data.extend(zip(pie_labels, [f"{p}%" for p in pie_data]))
    emotion_table = Table(emotion_data, hAlign='LEFT', colWidths=[200, 200])
    emotion_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(emotion_table)
    elements.append(Spacer(1, 24))

    # Generate chart images and add them to the PDF

    # Generate Pie Chart Image
    pie_chart_base64 = generate_chart_image(
        pie_labels,
        pie_data,
        chart_type='pie',
        title='Emotion Percentages'
    )
    pie_image_stream = io.BytesIO(base64.b64decode(pie_chart_base64))
    pie_image = Image(pie_image_stream, width=300, height=200)
    elements.append(Paragraph("Emotion Percentages Chart", styles['Heading2']))
    elements.append(pie_image)
    elements.append(Spacer(1, 24))

    # Generate Bar Chart for Emotion Distribution by Title (if 'title' column exists)
    if 'title' in df_statuses.columns:
        df_melted = df_statuses.melt(
            id_vars=['title'],
            value_vars=emotion_percentage_columns,
            var_name='emotion',
            value_name='percentage'
        )
        df_melted['emotion'] = df_melted['emotion'].str.replace('_percentage', '').str.capitalize()
        bar_chart_data = df_melted.groupby(['title', 'emotion'])['percentage'].mean().unstack().fillna(0).round(2)
        bar_labels = bar_chart_data.index.tolist()
        bar_data = [bar_chart_data[emotion].tolist() for emotion in pie_labels]

        # Adjust titles for length
        bar_labels = [title[:30] + '...' if len(title) > 30 else title for title in bar_labels]

        bar_chart_base64 = generate_chart_image(
            bar_labels,
            bar_data,
            chart_type='bar',
            title='Emotion Distribution by Title',
            dataset_labels=pie_labels
        )
        bar_image_stream = io.BytesIO(base64.b64decode(bar_chart_base64))
        bar_image = Image(bar_image_stream, width=700, height=300)
        elements.append(Paragraph("Emotion Distribution by Title", styles['Heading2']))
        elements.append(bar_image)
        elements.append(Spacer(1, 24))

        # Include data table for Bar Chart
        elements.append(Paragraph("Emotion Distribution by Title - Data", styles['Heading3']))
        bar_table_data = [['Title'] + pie_labels]
        for idx, title in enumerate(bar_labels):
            row = [title]
            row.extend([str(bar_chart_data.loc[bar_chart_data.index[idx], emotion]) for emotion in pie_labels])
            bar_table_data.append(row)
        bar_table = Table(bar_table_data, hAlign='LEFT', repeatRows=1)
        bar_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        elements.append(bar_table)
        elements.append(PageBreak())

    # Generate Line Chart for Emotion Trend Over Time (if 'created_at' column exists)
    if 'created_at' in df_statuses.columns:
        df_statuses['created_at'] = pd.to_datetime(df_statuses['created_at'])
        df_statuses['month_year'] = df_statuses['created_at'].dt.to_period('M').astype(str)
        sentiment_trends = df_statuses.groupby('month_year')[emotion_percentage_columns].mean().reset_index()
        line_labels = sentiment_trends['month_year'].tolist()
        line_data = [sentiment_trends[emotion].round(2).tolist() for emotion in emotion_percentage_columns]
        line_chart_base64 = generate_chart_image(
            line_labels,
            line_data,
            chart_type='line',
            title='Emotion Trend Over Time',
            dataset_labels=pie_labels
        )
        line_image_stream = io.BytesIO(base64.b64decode(line_chart_base64))
        line_image = Image(line_image_stream, width=700, height=300)
        elements.append(Paragraph("Emotion Trend Over Time", styles['Heading2']))
        elements.append(line_image)
        elements.append(Spacer(1, 24))

        # Include data table for Line Chart
        elements.append(Paragraph("Emotion Trend Over Time - Data", styles['Heading3']))
        line_table_data = [['Month/Year'] + pie_labels]
        for idx, month_year in enumerate(line_labels):
            row = [month_year]
            row.extend([str(sentiment_trends.loc[idx, emotion]) for emotion in emotion_percentage_columns])
            line_table_data.append(row)
        line_table = Table(line_table_data, hAlign='LEFT', repeatRows=1)
        line_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        elements.append(line_table)
        elements.append(PageBreak())

    # Generate Donut Chart for Emotion Intensity
    intensity_labels = ['Happiness', 'Neutral', 'Anger', 'Fear', 'Sadness']
    intensity_data = [
        int(df_statuses['happiness_percentage'].mean()) if 'happiness_percentage' in df_statuses.columns else 0,
        int(df_statuses['neutral_percentage'].mean()) if 'neutral_percentage' in df_statuses.columns else 0,
        int(df_statuses['anger_percentage'].mean()) if 'anger_percentage' in df_statuses.columns else 0,
        int(df_statuses['fear_percentage'].mean()) if 'fear_percentage' in df_statuses.columns else 0,
        int(df_statuses['sadness_percentage'].mean()) if 'sadness_percentage' in df_statuses.columns else 0,
    ]
    intensity_chart_base64 = generate_chart_image(
        intensity_labels,
        intensity_data,
        chart_type='doughnut',
        title='Emotion Intensity'
    )
    intensity_image_stream = io.BytesIO(base64.b64decode(intensity_chart_base64))
    intensity_image = Image(intensity_image_stream, width=300, height=200)
    elements.append(Paragraph("Emotion Intensity", styles['Heading2']))
    elements.append(intensity_image)
    elements.append(Spacer(1, 24))

    # Include data table for Emotion Intensity
    elements.append(Paragraph("Emotion Intensity - Data", styles['Heading3']))
    intensity_table_data = [['Emotion', 'Intensity']]
    intensity_table_data.extend(zip(intensity_labels, [str(value) for value in intensity_data]))
    intensity_table = Table(intensity_table_data, hAlign='LEFT', colWidths=[200, 200])
    intensity_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    elements.append(intensity_table)
    elements.append(Spacer(1, 24))

    # Generate Emotion Frequency Chart
    frequency_labels = [label.replace('_percentage', '').capitalize() for label in emotion_percentage_columns]
    if not df_statuses.empty:
        frequency_data = df_statuses[emotion_percentage_columns].count().tolist()
    else:
        frequency_data = [0 for _ in emotion_percentage_columns]
    frequency_chart_base64 = generate_chart_image(
        frequency_labels,
        frequency_data,
        chart_type='bar_single',
        title='Emotion Frequency'
    )
    frequency_image_stream = io.BytesIO(base64.b64decode(frequency_chart_base64))
    frequency_image = Image(frequency_image_stream, width=700, height=300)
    elements.append(Paragraph("Emotion Frequency", styles['Heading2']))
    elements.append(frequency_image)
    elements.append(Spacer(1, 24))

    # Include data table for Emotion Frequency
    elements.append(Paragraph("Emotion Frequency - Data", styles['Heading3']))
    frequency_table_data = [['Emotion', 'Frequency']]
    frequency_table_data.extend(zip(frequency_labels, [str(value) for value in frequency_data]))
    frequency_table = Table(frequency_table_data, hAlign='LEFT', colWidths=[200, 200])
    frequency_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    elements.append(frequency_table)
    elements.append(PageBreak())

    # Generate Emotion Pulse Chart
    if 'created_at' in df_statuses.columns and not df_statuses.empty:
        pulse_labels = sentiment_trends['month_year'].tolist()
        intensity_columns = ['happiness_percentage', 'neutral_percentage', 'anger_percentage', 'fear_percentage', 'sadness_percentage']
        pulse_data = [sentiment_trends[emotion].round(2).tolist() for emotion in intensity_columns]
        pulse_chart_base64 = generate_chart_image(
            pulse_labels,
            pulse_data,
            chart_type='area',
            title='Emotion Pulse',
            dataset_labels=intensity_labels
        )
        pulse_image_stream = io.BytesIO(base64.b64decode(pulse_chart_base64))
        pulse_image = Image(pulse_image_stream, width=700, height=300)
        elements.append(Paragraph("Emotion Pulse", styles['Heading2']))
        elements.append(pulse_image)
        elements.append(Spacer(1, 24))

        # Include data table for Emotion Pulse
        elements.append(Paragraph("Emotion Pulse - Data", styles['Heading3']))
        pulse_table_data = [['Month/Year'] + intensity_labels]
        for idx, month_year in enumerate(pulse_labels):
            row = [month_year]
            row.extend([str(sentiment_trends.loc[idx, emotion]) for emotion in intensity_columns])
            pulse_table_data.append(row)
        pulse_table = Table(pulse_table_data, hAlign='LEFT', repeatRows=1)
        pulse_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        elements.append(pulse_table)
        elements.append(PageBreak())

    # Generate Word Cloud
    if 'plain_description' in df_statuses.columns and not df_statuses['plain_description'].isnull().all():
        text = " ".join(df_statuses['plain_description'].astype(str).tolist())
        wordcloud_image_base64 = generate_wordcloud_image(text)
        wordcloud_image_stream = io.BytesIO(base64.b64decode(wordcloud_image_base64))
        wordcloud_image = Image(wordcloud_image_stream, width=700, height=300)
        elements.append(Paragraph("Word Cloud", styles['Heading2']))
        elements.append(wordcloud_image)
        elements.append(Spacer(1, 24))

    # Build and return the PDF
    doc.build(elements)
    return response


def generate_chart_image(labels, data, chart_type='pie', title='', dataset_labels=None):
    """
    Generates a chart based on the provided data and returns it as a base64-encoded image.
    """
    fig, ax = plt.subplots(figsize=(12, 6))  # Increased figure size for better readability
    if chart_type == 'bar':
        x = np.arange(len(labels))
        num_datasets = len(data)
        width = 0.8 / num_datasets
        for i, dataset in enumerate(data):
            offset = (i - (num_datasets - 1) / 2) * width
            label = dataset_labels[i] if dataset_labels and i < len(dataset_labels) else f'Dataset {i+1}'
            ax.bar(x + offset, dataset, width, label=label)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_title(title)
        ax.legend()
        plt.tight_layout()
    elif chart_type == 'bar_single':
        ax.bar(labels, data)
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_title(title)
        plt.tight_layout()
    elif chart_type == 'pie':
        ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title(title)
    elif chart_type == 'line':
        for i, dataset in enumerate(data):
            label = dataset_labels[i] if dataset_labels and i < len(dataset_labels) else f'Dataset {i+1}'
            ax.plot(labels, dataset, label=label)
        ax.set_xticks(np.arange(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_title(title)
        ax.legend()
        plt.tight_layout()
    elif chart_type == 'doughnut':
        wedges, _, autotexts = ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        for wedge in wedges:
            wedge.set_linewidth(2)
        center_circle = plt.Circle((0, 0), 0.70, color='white')
        ax.add_artist(center_circle)
        ax.set_title(title)
    elif chart_type == 'area':
        for i, dataset in enumerate(data):
            label = dataset_labels[i] if dataset_labels and i < len(dataset_labels) else f'Dataset {i+1}'
            ax.fill_between(labels, dataset, label=label, alpha=0.5)
        ax.set_xticks(np.arange(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_title(title)
        ax.legend()
        plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return image_base64

def generate_wordcloud_image(text):
    """
    Generates a word cloud image from the given text and returns it as a base64-encoded string.
    """
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    buf = io.BytesIO()
    wordcloud.to_image().save(buf, format='PNG')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return image_base64


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
    """
    Remastered Analysis View:
    - Separates Contextual Emotion Comparison from search filtering.
    - Adds independent search filtering and pagination for the comparison table.
    - Maintains Statuses and Keywords or Topics Detection functionalities.
    """
    # -------------------------
    # Statuses Management
    # -------------------------
    statuses_search_query = request.GET.get('search_status', '')
    category_status = request.GET.get('category_status', 'all')
    statuses_page_number = request.GET.get('page_statuses', 1)
    statuses_page_size = 10  # Adjust as needed

    # Filter statuses based on search query and category
    if category_status == 'all':
        statuses_queryset = Status.objects.filter(
            Q(title__icontains=statuses_search_query) |
            Q(plain_description__icontains=statuses_search_query)
        )
    else:
        statuses_queryset = Status.objects.filter(
            Q(title__icontains=statuses_search_query) |
            Q(plain_description__icontains=statuses_search_query),
            emotion=category_status
        )

    # Paginate statuses
    statuses_paginator = Paginator(statuses_queryset, statuses_page_size)
    statuses_page_obj = statuses_paginator.get_page(statuses_page_number)

    # -------------------------
    # Keywords or Topics Detection
    # -------------------------
    # Function to extract keywords from text
    def extract_keywords(text, num_keywords=5):
        tokens = word_tokenize(text.lower())
        stop_words_set = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words_set]
        word_counts = Counter(filtered_tokens)
        common_words = [word for word, count in word_counts.most_common(num_keywords)]
        return common_words

    # Extract keywords for each status in the current page
    keywords_data = []
    for status in statuses_page_obj:
        keywords = extract_keywords(status.plain_description)
        keywords_data.append({
            'status_id': status.id,
            'keywords': keywords
        })

    

    context = {
        # Statuses Management
        'statuses': statuses_page_obj,
        'statuses_search_query': statuses_search_query,
        'category_status': category_status,
        'statuses_page_obj': statuses_page_obj,

        # Keywords or Topics Detection
        'keywords_data': keywords_data,

        # Any additional context variables as needed
    }

    return render(request, 'admin_tools/analysis.html', context)

def delete_status(request, status_id):
    """
    Deletes a status given its ID.
    Only accessible by authenticated users.
    """
    status = get_object_or_404(Status, id=status_id)
    status.delete()
    messages.success(request, f'Status ID {status_id} has been deleted successfully.')
    return redirect('analysis')
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
@user_passes_test(is_counselor)
def comparison(request):
    """
    Contextual Emotion Comparison:
    - Compares each user's latest emotion status with their average emotions.
    - Includes independent search filtering and pagination for the comparison table.
    """
    comparison_search_query = request.GET.get('search_comparison', '')
    comparison_page_number = request.GET.get('page_comparison', 1)
    comparison_page_size = 10  # Number of users per page

    # Fetch users who are not counselors and have at least one status
    comparison_users = CustomUser.objects.filter(is_counselor=False).annotate(
        status_count=Count('status')
    ).filter(status_count__gte=1)

    # Apply search filter
    if comparison_search_query:
        comparison_users = comparison_users.filter(
            Q(username__icontains=comparison_search_query) |
            Q(full_name__icontains=comparison_search_query)
        )

    # Paginate the comparison users
    comparison_paginator = Paginator(comparison_users, comparison_page_size)
    comparison_page_obj = comparison_paginator.get_page(comparison_page_number)

    # Prepare comparison data
    comparison_data = []
    for user in comparison_page_obj:
        latest_status = Status.objects.filter(user=user).order_by('-created_at').first()
        if latest_status:
            # Calculate average emotions across all statuses
            average_emotions = Status.objects.filter(user=user).aggregate(
                avg_anger=Avg('anger_percentage'),
                avg_disgust=Avg('disgust_percentage'),
                avg_fear=Avg('fear_percentage'),
                avg_neutral=Avg('neutral_percentage'),
                avg_happiness=Avg('happiness_percentage'),
                avg_sadness=Avg('sadness_percentage'),
                avg_surprise=Avg('surprise_percentage'),
            )
            comparison = {
                'user_full_name': user.full_name,
                'latest_status': {
                    'anger': latest_status.anger_percentage,
                    'disgust': latest_status.disgust_percentage,
                    'fear': latest_status.fear_percentage,
                    'neutral': latest_status.neutral_percentage,
                    'happiness': latest_status.happiness_percentage,
                    'sadness': latest_status.sadness_percentage,
                    'surprise': latest_status.surprise_percentage,
                },
                'average_emotions': {
                    'anger': round(average_emotions['avg_anger'] or 0, 2),
                    'disgust': round(average_emotions['avg_disgust'] or 0, 2),
                    'fear': round(average_emotions['avg_fear'] or 0, 2),
                    'neutral': round(average_emotions['avg_neutral'] or 0, 2),
                    'happiness': round(average_emotions['avg_happiness'] or 0, 2),
                    'sadness': round(average_emotions['avg_sadness'] or 0, 2),
                    'surprise': round(average_emotions['avg_surprise'] or 0, 2),
                }
            }
            comparison_data.append(comparison)

    context = {
        'comparison_data': comparison_data,
        'comparison_search_query': comparison_search_query,
        'comparison_page_obj': comparison_page_obj,
    }

    return render(request, 'admin_tools/comparison.html', context)

@login_required
def data(request):
    if not request.user.is_counselor:
        return redirect('admin_login')

    # Dashboard Overview Data (from previous implementation)
    total_datasets = Dataset.objects.count()
    datasets_processing = Dataset.objects.filter(status='processing').count()
    datasets_completed = Dataset.objects.filter(status='completed').count()
    datasets_failed = Dataset.objects.filter(status='failed').count()

    performance_results = PerformanceResult.objects.all()
    if performance_results.exists():
        avg_accuracy = performance_results.aggregate(Avg('accuracy'))['accuracy__avg']
        avg_precision = performance_results.aggregate(Avg('precision'))['precision__avg']
        avg_recall = performance_results.aggregate(Avg('recall'))['recall__avg']
        avg_f1_score = performance_results.aggregate(Avg('f1_score'))['f1_score__avg']
    else:
        avg_accuracy = avg_precision = avg_recall = avg_f1_score = None

    recent_datasets = Dataset.objects.order_by('-uploaded_at')[:5]
    recent_activities = []
    for dataset in recent_datasets:
        recent_activities.append({
            'user': dataset.user.get_full_name(),
            'action': 'Uploaded a dataset',
            'timestamp': dataset.uploaded_at,
        })

    # Data Table Search and Filtering
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    user_filter = request.GET.get('user', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    date_range = request.GET.get('date_range', '')

    datasets = Dataset.objects.all()

    # Filtering by search query
    if search_query:
        datasets = datasets.filter(
            Q(name__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )

    # Filtering by status
    if status_filter:
        datasets = datasets.filter(status=status_filter)

    # Filtering by user
    if user_filter:
        datasets = datasets.filter(user__id=user_filter)

    # Filtering by date range
    if date_range:
        # Parse the date_range string
        try:
            start_date_str, end_date_str = date_range.split(' - ')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            # Adjust end_date to include the entire day
            end_date = end_date + timedelta(days=1)
            datasets = datasets.filter(uploaded_at__range=(start_date, end_date))
        except ValueError:
            # Handle invalid date format
            pass

        # Check if 'export' parameter is in GET request
    if 'export' in request.GET:
        export_format = request.GET.get('export')
        datasets_to_export = datasets.order_by('-uploaded_at')

        if export_format == 'csv':
            return export_datasets_csv(datasets_to_export)
        elif export_format == 'zip':
            return export_datasets_zip(datasets_to_export)
        elif export_format == 'performance':
            return export_performance_report(request, datasets_to_export)
        elif export_format == 'error_logs':
            return export_error_logs(request, datasets_to_export)  # Add 'request' as the first argument
        else:
            messages.error(request, 'Invalid export format specified.')
            return redirect('admin_data')

    # Pagination
    paginator = Paginator(datasets.order_by('-uploaded_at'), 10)  # 10 datasets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Users for filtering dropdown
    users = CustomUser.objects.filter(is_counselor=False)

    context = {
        # Dashboard Overview Data
        'total_datasets': total_datasets,
        'datasets_processing': datasets_processing,
        'datasets_completed': datasets_completed,
        'datasets_failed': datasets_failed,
        'avg_accuracy': avg_accuracy,
        'avg_precision': avg_precision,
        'avg_recall': avg_recall,
        'avg_f1_score': avg_f1_score,
        'recent_activities': recent_activities,

        # Data Table Context
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'user_filter': user_filter,
        'date_range': date_range,
        'users': users,
    }
    return render(request, 'admin_tools/data.html', context)

def export_datasets_csv(datasets):
    # Create the HttpResponse object with CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="datasets.csv"'

    writer = csv.writer(response)
    # Write headers
    writer.writerow(['Dataset Name', 'Upload Date', 'User', 'Status'])
    # Write data
    for dataset in datasets:
        writer.writerow([
            dataset.name,
            dataset.uploaded_at.strftime('%Y-%m-%d %H:%M'),
            dataset.user.get_full_name(),
            dataset.get_status_display(),
        ])
    return response

def export_datasets_zip(datasets):
    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for dataset in datasets:
            file_path = dataset.csv_file.path
            if os.path.exists(file_path):
                zip_file.write(file_path, arcname=os.path.basename(file_path))
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="datasets.zip"'
    return response

def export_performance_report(request, datasets):
    # Collect performance data
    performance_data = []
    for dataset in datasets:
        performance = getattr(dataset, 'performance_result', None)
        if performance:
            performance_data.append({
                'Dataset Name': dataset.name,
                'Accuracy': performance.accuracy,
                'Precision': performance.precision,
                'Recall': performance.recall,
                'F1 Score': performance.f1_score,
            })
    if not performance_data:
        messages.error(request, 'No performance data available for the selected datasets.')
        return redirect('admin_data')

    # Create a DataFrame and export to Excel
    df = pd.DataFrame(performance_data)
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Performance Report')
    excel_buffer.seek(0)
    response = HttpResponse(
        excel_buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="performance_report.xlsx"'
    return response

def export_error_logs(request, datasets):
    # Collect error logs from datasets with 'failed' status
    error_logs = []
    for dataset in datasets.filter(status='failed'):
        error_log = dataset.error_log  # Assuming you have an 'error_log' field
        if error_log:
            error_logs.append({
                'Dataset Name': dataset.name,
                'Error Log': error_log,
            })

    if not error_logs:
        messages.error(request, 'No error logs available for the selected datasets.')
        return redirect('admin_data')

    # Create a text file with error logs
    error_logs_content = ''
    for log in error_logs:
        error_logs_content += f"Dataset: {log['Dataset Name']}\n"
        error_logs_content += f"Error Log:\n{log['Error Log']}\n"
        error_logs_content += '-' * 50 + '\n'

    response = HttpResponse(error_logs_content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="error_logs.txt"'
    return response

@login_required
def dataset_detail(request, dataset_id):
    if not request.user.is_counselor:
        return redirect('admin_login')

    dataset = get_object_or_404(Dataset, id=dataset_id)
    performance = getattr(dataset, 'performance_result', None)

    # Generate dataset preview
    import pandas as pd
    preview_data = None
    try:
        df = pd.read_csv(dataset.csv_file.path)
        preview_data = {
            'columns': df.columns.tolist(),
            'rows': df.head(5).values.tolist()
        }
    except Exception as e:
        # Handle exception if the file cannot be read
        pass

    context = {
        'dataset': dataset,
        'performance': performance,
        'preview_data': preview_data,
    }
    return render(request, 'admin_tools/dataset_detail.html', context)

@login_required
def download_dataset(request, dataset_id):
    if not request.user.is_counselor:
        return redirect('admin_login')

    dataset = get_object_or_404(Dataset, id=dataset_id)
    file_path = dataset.csv_file.path

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    else:
        raise Http404

@login_required
def delete_dataset(request, dataset_id):
    if not request.user.is_counselor:
        return redirect('admin_login')

    dataset = get_object_or_404(Dataset, id=dataset_id)
    dataset.delete()
    messages.success(request, 'Dataset deleted successfully.')
    return redirect('admin_data')


@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
