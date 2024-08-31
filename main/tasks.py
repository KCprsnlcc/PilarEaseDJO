from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import os
from django.conf import settings
from email.mime.image import MIMEImage

@shared_task
def send_password_reset_email(user_email, email_subject, email_html_content):
    email_text_content = strip_tags(email_html_content)

    email_message = EmailMultiAlternatives(
        email_subject,
        email_text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )
    email_message.attach_alternative(email_html_content, "text/html")

    logo_path = os.path.join(settings.STATIC_ROOT, 'images/PilarLogo.png')
    with open(logo_path, 'rb') as logo_file:
        logo_image = MIMEImage(logo_file.read())
        logo_image.add_header('Content-ID', '<PilarLogo>')
        email_message.attach(logo_image)

    ease_logo_path = os.path.join(settings.STATIC_ROOT, 'images/PilarEaseLogo.png')
    with open(ease_logo_path, 'rb') as ease_logo_file:
        ease_logo_image = MIMEImage(ease_logo_file.read())
        ease_logo_image.add_header('Content-ID', '<PilarEaseLogo>')
        email_message.attach(ease_logo_image)

    email_message.send()
