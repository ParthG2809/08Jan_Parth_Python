from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from .models import User, OTP
from .forms import SignupForm, OTPVerifyForm, LoginForm

class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('accounts:verify_otp')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        
        # Generate and Send OTP
        otp_code = OTP.generate_otp()
        OTP.objects.create(user=user, otp=otp_code)
        
        # Prepare HTML Email
        subject = 'Verify your Reddit Account'
        from_email = 'noreply@reddit.com'
        to = [user.email]
        
        html_content = render_to_string('emails/otp_email.html', {
            'fullname': user.fullname,
            'otp': otp_code
        })
        text_content = strip_tags(html_content)
        
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        # Store user ID in session
        self.request.session['unverified_user_id'] = user.id
        messages.success(self.request, "Account created! Please verify your OTP sent to your email.")
        return super().form_valid(form)

class OTPVerifyView(FormView):
    template_name = 'accounts/otp_verify.html'
    form_class = OTPVerifyForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user_id = self.request.session.get('unverified_user_id')
        if not user_id:
            messages.error(self.request, "Session expired. Please signup again.")
            return redirect('accounts:signup')
        
        try:
            user = User.objects.get(id=user_id)
            otp_obj = OTP.objects.get(user=user)
            
            if otp_obj.otp == form.cleaned_data['otp']:
                if not otp_obj.is_expired():
                    user.is_active = True
                    user.save()
                    otp_obj.delete()
                    del self.request.session['unverified_user_id']
                    messages.success(self.request, "Email verified successfully! You can now login.")
                    return super().form_valid(form)
                else:
                    messages.error(self.request, "OTP expired.")
            else:
                messages.error(self.request, "Invalid OTP.")
        except (User.DoesNotExist, OTP.DoesNotExist):
            messages.error(self.request, "Verification failed.")
            
        return self.form_invalid(form)

class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('feed:home')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.success(self.request, f"Welcome back, {user.fullname}!")
                return super().form_valid(form)
            else:
                self.request.session['unverified_user_id'] = user.id
                messages.warning(self.request, "Your account is not verified. Please verify your OTP.")
                return redirect('accounts:verify_otp')
        else:
            messages.error(self.request, "Invalid email or password.")
            return self.form_invalid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Logged out successfully.")
        return redirect('accounts:login')
