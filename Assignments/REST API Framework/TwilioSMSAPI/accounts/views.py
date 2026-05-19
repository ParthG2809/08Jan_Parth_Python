from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from twilio.rest import Client
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def register(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        username = request.POST.get('username')
        
        if not phone_number or not username:
            messages.error(request, 'Please provide both username and phone number.')
            return render(request, 'accounts/register.html')
        
        # Generate OTP
        otp = generate_otp()
        
        # Store in session
        request.session['registration_data'] = {
            'username': username,
            'phone_number': phone_number,
            'otp': otp
        }
        
        try:
            # Send OTP via Twilio
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your registration OTP is: {otp}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            messages.success(request, f'OTP sent to {phone_number}. Please verify.')
            return redirect('verify')
        except Exception as e:
            messages.error(request, f'Failed to send OTP: {str(e)}')
            return render(request, 'accounts/register.html')
            
    return render(request, 'accounts/register.html')

def verify(request):
    registration_data = request.session.get('registration_data')
    if not registration_data:
        messages.error(request, 'Session expired or invalid. Please register again.')
        return redirect('register')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        if entered_otp == registration_data.get('otp'):
            # Create user logic here, e.g., using Django's User model
            from django.contrib.auth.models import User
            
            username = registration_data['username']
            # We skip password creation for simplicity, or we could have taken a password in registration.
            # Let's create user with username
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username)
                user.save()
                messages.success(request, 'Registration successful! Your phone number is verified.')
                # Clear session
                del request.session['registration_data']
                return redirect('register') # Redirect to login or home in a real app
            else:
                messages.error(request, 'Username already exists. Please choose a different one.')
                return redirect('register')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            
    return render(request, 'accounts/verify.html')
