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
import matplotlib
matplotlib.use('Agg')  # Must be set before importing pyplot
import base64 
import matplotlib.pyplot as plt
import io
from django.core.files.base import ContentFile
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
    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            dataset = form.save(commit=False)
            dataset.user = request.user
            dataset.progress = {'current_task': 'Uploading', 'percentage': 0}
            dataset.save()

            # Start background thread for processing
            thread = threading.Thread(target=process_dataset, args=(dataset.id,))
            thread.start()

            # Redirect to the same page with dataset_id
            return redirect(f"{reverse('performance_dashboard')}?dataset_id={dataset.id}")
    else:
        form = DatasetUploadForm()
        dataset_id = request.GET.get('dataset_id')
        performance_result = None

        if dataset_id:
            dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)
            # Check if processing is complete
            if dataset.progress.get('percentage') == 100:
                try:
                    performance_result = PerformanceResult.objects.get(dataset=dataset)
                except PerformanceResult.DoesNotExist:
                    messages.error(request, "Performance results not found.")
            else:
                # Processing is still in progress
                pass  # The template will handle displaying the progress bar
        else:
            # Optionally, check for the latest performance result
            try:
                latest_dataset = Dataset.objects.filter(user=request.user).latest('uploaded_at')
                if latest_dataset.progress.get('percentage') == 100:
                    performance_result = PerformanceResult.objects.get(dataset=latest_dataset)
            except (Dataset.DoesNotExist, PerformanceResult.DoesNotExist):
                pass

    # Handle search and pagination if performance_result is available
    page_obj = None
    search_query = ''
    if performance_result and performance_result.processed_csv_file:
        # Read the processed dataset and its TextAnalysis records
        text_analyses = TextAnalysis.objects.filter(dataset=dataset)

        # Apply search filter if provided
        search_query = request.GET.get('search', '')
        if search_query:
            text_analyses = text_analyses.filter(
                Q(text__icontains=search_query) |
                Q(actual_label__icontains=search_query) |
                Q(predicted_label__icontains(search_query))
            )

        # Paginate the data
        paginator = Paginator(text_analyses, 10)  # Show 10 entries per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    elif performance_result:
        messages.error(request, "Processed dataset not available.")

    context = {
        'form': form,
        'dataset_id': dataset_id,
        'performance_result': performance_result,
        'page_obj': page_obj,
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
                        'surprise': scores[6]
                    }

                    # Get the emotion with the highest score
                    predicted_label = max(emotions, key=emotions.get)
                y_pred.append(predicted_label)
            else:
                y_pred.append(None)

            # Update progress every 10%
            current_percentage = 40 + int((len(y_pred) / total) * 60)
            dataset.progress = {'current_task': 'Making Predictions', 'percentage': current_percentage}
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
        report_html = report_df.to_html(classes='pilarease-admin-classification-report-table', border=0)
        report_csv = report_df.to_csv(index=True)
        report_csv_base64 = base64.b64encode(report_csv.encode('utf-8')).decode('utf-8')

        # Plot confusion matrix
        plt.figure(figsize=(8,6))
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

        # Save individual analyses to the database using JSONB
        for idx, actual_label, predicted_label in zip(y_test_clean.index, y_test_clean, y_pred_clean):
            text = df.loc[idx, 'Text']
            analysis_data = {
                "text": text,
                "actual_label": actual_label,
                "predicted_label": predicted_label
            }
            analysis = TextAnalysis(
                dataset=dataset,
                analysis_data=analysis_data  # Save all data in JSONB
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
            save=True
        )

        # Final progress update
        dataset.progress = {'current_task': 'Completed', 'percentage': 100, 'result_id': performance_result.id}
        dataset.save()

    except Exception as e:
        logger.exception(f"Error processing dataset {dataset_id}: {e}")
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            dataset.progress = {'current_task': f'Error: {str(e)}', 'percentage': 100}
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
    referrals = Referral.objects.select_related('status', 'referred_by__profile').all().order_by('-created_at')
    profanity_words = ProfanityWord.objects.first()
    profanities = profanity_words.word_list if profanity_words else []
    context = {
        'referrals': referrals,
        'profanities': profanities,
    }
    return render(request, 'admin_tools/referral.html', context)

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

@login_required
@user_passes_test(is_counselor)
@require_http_methods(["POST"])
def add_profanity(request):
    try:
        payload = json.loads(request.body)
        new_word = payload.get("word", "").strip().lower()
        if not new_word:
            return HttpResponseBadRequest("Word cannot be empty.")
        
        profanity_words, created = ProfanityWord.objects.get_or_create(id=1)  # Assuming a single ProfanityWord entry
        if new_word not in profanity_words.word_list:
            profanity_words.word_list.append(new_word)
            profanity_words.save()
            return JsonResponse({"status": "success", "message": f"'{new_word}' added to profanity list."})
        else:
            return HttpResponseBadRequest("Word already exists in the profanity list.")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON.")

@login_required
@user_passes_test(is_counselor)
@require_http_methods(["POST"])
def delete_profanity(request, profanity_id):
    try:
        profanity_words = ProfanityWord.objects.first()
        if profanity_words and 0 <= profanity_id < len(profanity_words.word_list):
            removed_word = profanity_words.word_list.pop(profanity_id)
            profanity_words.save()
            return JsonResponse({"status": "success", "message": f"'{removed_word}' removed from profanity list."})
        else:
            return HttpResponseBadRequest("Invalid profanity ID.")
    except Exception as e:
        return HttpResponseBadRequest(str(e))

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
    return add_profanity(request)

@login_required
@user_passes_test(is_counselor)
def delete_profanity_api(request, profanity_id):
    return delete_profanity(request, profanity_id)


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
