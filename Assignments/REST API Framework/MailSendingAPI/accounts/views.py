from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send confirmation email
            subject = 'Welcome to Our Service!'
            message = f'Hi {user.username},\n\nThank you for registering on our platform! We are excited to have you.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, 'Account created successfully. A confirmation email has been sent to your inbox.')
            except Exception as e:
                messages.error(request, f'Account created, but failed to send email: {str(e)}')
            
            return redirect('register')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/register.html', {'form': form})
