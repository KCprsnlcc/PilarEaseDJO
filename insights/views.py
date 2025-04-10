from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from main.models import CustomUser, Status
from django.http import JsonResponse, HttpResponse
import json
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch

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
    Displays the user's latest status and emotional trends over time.
    Includes comparative analytics and keyword extraction.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Get all statuses for this user, ordered by creation date
    statuses = Status.objects.filter(user=user).order_by('-created_at')
    latest_status = statuses.first()
    statuses_count = statuses.count()
    
    # Count critical emotional states
    CRITICAL_THRESHOLD = 70
    critical = False
    concerning_emotions = []
    critical_count = 0
    
    # Calculate average time between statuses if there are multiple statuses
    avg_days_between_statuses = None
    if statuses_count > 1:
        # Convert QuerySet to list to access by index
        statuses_list = list(statuses)
        total_days = 0
        for i in range(statuses_count - 1):
            days_diff = (statuses_list[i].created_at - statuses_list[i + 1].created_at).days
            total_days += days_diff
        avg_days_between_statuses = round(total_days / (statuses_count - 1), 1)
    
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
        
        # Count all critical statuses
        for status in statuses:
            if (status.anger_percentage >= CRITICAL_THRESHOLD or 
                status.sadness_percentage >= CRITICAL_THRESHOLD or 
                status.fear_percentage >= CRITICAL_THRESHOLD or 
                status.disgust_percentage >= CRITICAL_THRESHOLD):
                critical_count += 1
    
    # Check for potentially problematic content
    flagged_words = []
    if latest_status:
        from main.views import load_custom_profanities
        profanity_list = load_custom_profanities()
        if profanity_list:
            for word in profanity_list:
                if word.lower() in latest_status.description.lower():
                    flagged_words.append(word)
    
    # Calculate emotion trends over time (for chart)
    dates = []
    anger_trends = []
    sadness_trends = []
    fear_trends = []
    happiness_trends = []
    
    # Limit to the last 10 statuses for the chart
    chart_statuses = statuses[:10]
    for status in reversed(chart_statuses):  # Reverse to show chronological order
        dates.append(status.created_at.strftime('%Y-%m-%d'))
        anger_trends.append(status.anger_percentage)
        sadness_trends.append(status.sadness_percentage)
        fear_trends.append(status.fear_percentage)
        happiness_trends.append(status.happiness_percentage)
    
    # Calculate average emotions across all statuses
    avg_emotions = {
        'anger': 0,
        'disgust': 0,
        'fear': 0,
        'happiness': 0,
        'sadness': 0,
        'surprise': 0,
        'neutral': 0
    }
    
    if statuses_count > 0:
        for status in statuses:
            avg_emotions['anger'] += status.anger_percentage
            avg_emotions['disgust'] += status.disgust_percentage
            avg_emotions['fear'] += status.fear_percentage
            avg_emotions['happiness'] += status.happiness_percentage
            avg_emotions['sadness'] += status.sadness_percentage
            avg_emotions['surprise'] += status.surprise_percentage
            avg_emotions['neutral'] += status.neutral_percentage
        
        for emotion in avg_emotions:
            avg_emotions[emotion] = round(avg_emotions[emotion] / statuses_count)
    
    # Extract keywords for keyword cloud
    import re
    from collections import Counter
    
    keywords = []
    if statuses_count > 0:
        # Combine all status descriptions
        all_text = " ".join([status.plain_description for status in statuses if status.plain_description])
        
        # Remove common stop words and punctuation
        stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
                      'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 
                      'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 
                      'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
                      'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
                      'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 
                      'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 
                      'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
                      'with', 'about', 'against', 'between', 'into', 'through', 'during', 
                      'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
                      'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 
                      'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 
                      'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 
                      'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
                      'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 
                      'should', 'now']
        
        # Clean text and split into words
        cleaned_text = re.sub(r'[^\w\s]', '', all_text.lower())
        words = cleaned_text.split()
        words = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Count word frequency
        word_counts = Counter(words)
        most_common = word_counts.most_common(20)  # Get top 20 keywords
        
        # Calculate font sizes based on frequency (min size 14, max size 28)
        max_count = most_common[0][1] if most_common else 1
        min_count = most_common[-1][1] if most_common else 1
        
        for word, count in most_common:
            # Calculate relative size (14-28px range)
            if max_count == min_count:  # Avoid division by zero
                size = 20
            else:
                size = 14 + (count - min_count) * 14 / (max_count - min_count)
            
            keywords.append({
                'text': word,
                'size': round(size)
            })
    
    import json
    context = {
        'user': user,
        'latest_status': latest_status,
        'statuses': statuses,
        'statuses_count': statuses_count,
        'avg_days_between_statuses': avg_days_between_statuses,
        'critical': critical,
        'critical_count': critical_count,
        'concerning_emotions': concerning_emotions,
        'flagged_words': flagged_words,
        'dates_json': json.dumps(dates),
        'anger_trends': json.dumps(anger_trends),
        'sadness_trends': json.dumps(sadness_trends),
        'fear_trends': json.dumps(fear_trends),
        'happiness_trends': json.dumps(happiness_trends),
        'avg_emotions': avg_emotions,
        'keywords': keywords
    }
    return render(request, 'insights/user_analysis.html', context)

@login_required
def status_details_api(request, status_id):
    """
    API endpoint that returns status details in JSON format for the modal view.
    """
    status = get_object_or_404(Status, id=status_id)
    
    # Format the data for the modal
    status_data = {
        'id': status.id,
        'title': status.title,
        'description': status.description,
        'plain_description': status.plain_description,
        'created_at': status.created_at.strftime("%B %d, %Y, %I:%M %p"),
        'emotion': status.emotion,
        'anger_percentage': status.anger_percentage,
        'disgust_percentage': status.disgust_percentage,
        'fear_percentage': status.fear_percentage,
        'happiness_percentage': status.happiness_percentage,
        'sadness_percentage': status.sadness_percentage,
        'surprise_percentage': status.surprise_percentage,
        'neutral_percentage': status.neutral_percentage
    }
    
    return JsonResponse(status_data)

@login_required
def generate_user_report(request, user_id):
    """
    Generates a PDF report for a user's emotional analysis.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Get all statuses for this user, ordered by creation date
    statuses = Status.objects.filter(user=user).order_by('-created_at')
    latest_status = statuses.first()
    statuses_count = statuses.count()
    
    # Count critical emotional states
    CRITICAL_THRESHOLD = 70
    critical = False
    concerning_emotions = []
    critical_count = 0
    
    # Calculate average time between statuses if there are multiple statuses
    avg_days_between_statuses = None
    if statuses_count > 1:
        # Convert QuerySet to list to access by index
        statuses_list = list(statuses)
        total_days = 0
        for i in range(statuses_count - 1):
            days_diff = (statuses_list[i].created_at - statuses_list[i + 1].created_at).days
            total_days += days_diff
        avg_days_between_statuses = round(total_days / (statuses_count - 1), 1)
    
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
        
        # Count all critical statuses
        for status in statuses:
            if (status.anger_percentage >= CRITICAL_THRESHOLD or 
                status.sadness_percentage >= CRITICAL_THRESHOLD or 
                status.fear_percentage >= CRITICAL_THRESHOLD or 
                status.disgust_percentage >= CRITICAL_THRESHOLD):
                critical_count += 1
    
    # Calculate average emotions across all statuses
    avg_emotions = {
        'anger': 0,
        'disgust': 0,
        'fear': 0,
        'happiness': 0,
        'sadness': 0,
        'surprise': 0,
        'neutral': 0
    }
    
    if statuses_count > 0:
        for status in statuses:
            avg_emotions['anger'] += status.anger_percentage
            avg_emotions['disgust'] += status.disgust_percentage
            avg_emotions['fear'] += status.fear_percentage
            avg_emotions['happiness'] += status.happiness_percentage
            avg_emotions['sadness'] += status.sadness_percentage
            avg_emotions['surprise'] += status.surprise_percentage
            avg_emotions['neutral'] += status.neutral_percentage
        
        for emotion in avg_emotions:
            avg_emotions[emotion] = round(avg_emotions[emotion] / statuses_count)
    
    # Create PDF report
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading1"]
    subheading_style = styles["Heading2"]
    normal_style = styles["Normal"]
    
    # Custom styles
    warning_style = ParagraphStyle(
        'WarningStyle', 
        parent=normal_style,
        textColor=colors.red,
        spaceAfter=12
    )
    
    timestamp_style = ParagraphStyle(
        'TimestampStyle',
        parent=normal_style,
        fontSize=8,
        textColor=colors.grey,
        alignment=1  # Center alignment
    )
    
    # Create elements list for the PDF
    elements = []
    
    # Add title
    elements.append(Paragraph(f"Emotional Analysis Report: {user.full_name}", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add timestamp
    report_date = datetime.now().strftime("%B %d, %Y, %I:%M %p")
    elements.append(Paragraph(f"Generated on: {report_date}", timestamp_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # User overview section
    elements.append(Paragraph("User Overview", heading_style))
    
    # Summary data in a table
    summary_data = [
        ["Total Statuses", str(statuses_count)],
        ["Avg. Days Between", str(avg_days_between_statuses) if avg_days_between_statuses else "N/A"],
        ["Current Emotion", latest_status.emotion if latest_status else "N/A"],
        ["Critical States", str(critical_count)]
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Latest status section if available
    if latest_status:
        elements.append(Paragraph("Latest Status Analysis", heading_style))
        elements.append(Paragraph(f"Title: {latest_status.title}", subheading_style))
        elements.append(Paragraph(f"Created on: {latest_status.created_at.strftime('%B %d, %Y, %I:%M %p')}", normal_style))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("Description:", normal_style))
        elements.append(Paragraph(latest_status.plain_description, normal_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Critical alert if any
        if critical:
            elements.append(Paragraph(f"CRITICAL ALERT: Concerning emotional states detected: {', '.join(concerning_emotions)}", warning_style))
        
        # Emotion percentages in a table
        elements.append(Paragraph("Emotion Analysis", subheading_style))
        
        emotion_data = [
            ["Emotion", "Percentage"],
            ["Anger", f"{latest_status.anger_percentage}%"],
            ["Sadness", f"{latest_status.sadness_percentage}%"],
            ["Fear", f"{latest_status.fear_percentage}%"],
            ["Disgust", f"{latest_status.disgust_percentage}%"],
            ["Happiness", f"{latest_status.happiness_percentage}%"],
            ["Surprise", f"{latest_status.surprise_percentage}%"],
            ["Neutral", f"{latest_status.neutral_percentage}%"]
        ]
        
        emotion_table = Table(emotion_data, colWidths=[2*inch, 2*inch])
        emotion_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            # Highlight critical emotions
            ('BACKGROUND', (1, 1), (1, 1), colors.lightcoral if latest_status.anger_percentage >= CRITICAL_THRESHOLD else colors.white),
            ('BACKGROUND', (1, 2), (1, 2), colors.lightcoral if latest_status.sadness_percentage >= CRITICAL_THRESHOLD else colors.white),
            ('BACKGROUND', (1, 3), (1, 3), colors.lightcoral if latest_status.fear_percentage >= CRITICAL_THRESHOLD else colors.white),
            ('BACKGROUND', (1, 4), (1, 4), colors.lightcoral if latest_status.disgust_percentage >= CRITICAL_THRESHOLD else colors.white)
        ]))
        
        elements.append(emotion_table)
        elements.append(Spacer(1, 0.25*inch))
    
    # Historical averages
    elements.append(Paragraph("Historical Emotion Averages", heading_style))
    avg_emotion_data = [
        ["Emotion", "Average Percentage"],
        ["Anger", f"{avg_emotions['anger']}%"],
        ["Sadness", f"{avg_emotions['sadness']}%"],
        ["Fear", f"{avg_emotions['fear']}%"],
        ["Disgust", f"{avg_emotions['disgust']}%"],
        ["Happiness", f"{avg_emotions['happiness']}%"],
        ["Surprise", f"{avg_emotions['surprise']}%"],
        ["Neutral", f"{avg_emotions['neutral']}%"]
    ]
    
    avg_emotion_table = Table(avg_emotion_data, colWidths=[2*inch, 2*inch])
    avg_emotion_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(avg_emotion_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Status history section
    elements.append(Paragraph("Status History", heading_style))
    
    if statuses_count > 0:
        # Create table header
        history_data = [["Date", "Title", "Emotion", "Critical"]]
        
        # Add status data (limit to 15 most recent for space)
        for status in statuses[:15]:
            is_critical = (status.anger_percentage >= CRITICAL_THRESHOLD or 
                          status.sadness_percentage >= CRITICAL_THRESHOLD or 
                          status.fear_percentage >= CRITICAL_THRESHOLD or 
                          status.disgust_percentage >= CRITICAL_THRESHOLD)
            
            history_data.append([
                status.created_at.strftime('%m/%d/%Y'),
                status.title,
                status.emotion,
                "Yes" if is_critical else "No"
            ])
        
        # If there are more statuses than we showed
        if statuses_count > 15:
            history_data.append(["...", "...", "...", "..."])
            history_data.append([f"Total: {statuses_count} statuses", "", "", ""])
        
        # Create and style table
        history_table = Table(history_data, colWidths=[1*inch, 3*inch, 1*inch, 1*inch])
        history_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            # Handle truncation for long titles
            ('FONTSIZE', (1, 1), (1, -1), 8)
        ]))
        
        elements.append(history_table)
    else:
        elements.append(Paragraph("No status history available.", normal_style))
    
    # Recommendations or observations section
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Observations & Recommendations", heading_style))
    
    recommendations = []
    
    # Generate observations based on data
    if critical:
        recommendations.append(Paragraph("⚠️ Critical emotional states detected in the latest status. Consider scheduling a follow-up session.", warning_style))
    
    if statuses_count == 0:
        recommendations.append(Paragraph("No status data available. Encourage the user to share their emotional state.", normal_style))
    elif statuses_count < 3:
        recommendations.append(Paragraph("Limited status history. More data would help establish patterns.", normal_style))
    
    if avg_days_between_statuses and avg_days_between_statuses > 14:
        recommendations.append(Paragraph(f"Status updates are infrequent (average {avg_days_between_statuses} days apart). Consider encouraging more regular check-ins.", normal_style))
    
    if avg_emotions['happiness'] < 30:
        recommendations.append(Paragraph("Low average happiness detected across statuses. Consider using positive reinforcement techniques.", normal_style))
    
    if critical_count > statuses_count / 2:
        recommendations.append(Paragraph(f"High proportion of critical states ({critical_count} out of {statuses_count}). Consider intervention strategies.", warning_style))
    
    if not recommendations:
        recommendations.append(Paragraph("No specific observations at this time. Continue regular monitoring.", normal_style))
    
    for recommendation in recommendations:
        elements.append(recommendation)
    
    # Build the PDF
    doc.build(elements)
    
    # Prepare response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"user_analysis_{user.username}_{timestamp}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
