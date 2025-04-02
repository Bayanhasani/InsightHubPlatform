from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_verification_email(user, request):
    token = user.generate_verification_token()
    verification_link = request.build_absolute_uri(
        reverse('verify_email', kwargs={'token': token})
    )
    
    subject = "Mutah University: Verify Your Email Address"  # Specific subject
    message = f"""
    Dear {user.username},

    Please verify your email for Mutah University Community Hub by clicking:
    {verification_link}

    If you didn't request this, ignore this email.

    Best regards,
    Mutah University Team
    """
    html_message = f"""  # HTML version (optional)
    <p>Dear {user.username},</p>
    <p><a href="{verification_link}">Click here to verify</a></p>
    <p>Or copy this link: {verification_link}</p>
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )