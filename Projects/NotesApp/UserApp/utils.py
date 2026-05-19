from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import OTP

def send_otp_email(user):
    otp, created = OTP.objects.get_or_create(user=user)
    otp.generate_code()
    
    subject = 'Your NotesApp Verification Code'
    context = {
        'user': user,
        'otp_code': otp.code
    }
    
    html_message = render_to_string('emails/otp_email.html', context)
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER or 'noreply@notesapp.com'
    recipient_list = [user.email]
    
    send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
    return otp.code

def send_note_status_email(note):
    user = note.user
    subject = f'Your Note "{note.title}" has been {note.status}'
    context = {
        'user': user,
        'note': note,
    }
    
    html_message = render_to_string('emails/note_status_email.html', context)
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER or 'noreply@notesapp.com'
    recipient_list = [user.email]
    
    send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
def send_password_reset_otp(user):
    otp, created = OTP.objects.get_or_create(user=user)
    otp.generate_code()
    
    subject = 'Reset Your NotesApp Password'
    context = {'otp': otp.code}
    
    html_message = render_to_string('emails/reset_password_otp.html', context)
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER or 'noreply@notesapp.com'
    recipient_list = [user.email]
    
    send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
    return otp.code
