from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, ListView, UpdateView, DeleteView, View
import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, ListView, UpdateView, DeleteView, View
import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import CustomUser, OTP, Note
from AdminApp.models import ContactMessage
from .forms import SignupForm, LoginForm, NoteForm, UserProfileForm
from .utils import send_otp_email, send_password_reset_otp

class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'UserApp/forgot_password.html')

    def post(self, request):
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            send_password_reset_otp(user)
            request.session['reset_email'] = email
            messages.success(request, "Verification code sent to your email.")
            return redirect('verify_otp_reset')
        else:
            messages.error(request, "No account found with this email.")
        return render(request, 'UserApp/forgot_password.html')

class VerifyOTPResetView(View):
    def get(self, request):
        if 'reset_email' not in request.session:
            return redirect('forgot_password')
        return render(request, 'UserApp/verify_otp_reset.html')

    def post(self, request):
        email = request.session.get('reset_email')
        otp_code = request.POST.get('otp')
        user = CustomUser.objects.filter(email=email).first()
        
        if user:
            otp_obj = OTP.objects.filter(user=user, code=otp_code).first()
            if otp_obj and otp_obj.is_valid():
                request.session['otp_verified'] = True
                return redirect('reset_password')
            else:
                messages.error(request, "Invalid or expired verification code.")
        else:
            return redirect('forgot_password')
        return render(request, 'UserApp/verify_otp_reset.html')

class ResetPasswordView(View):
    def get(self, request):
        if not request.session.get('otp_verified'):
            return redirect('forgot_password')
        return render(request, 'UserApp/reset_password.html')

    def post(self, request):
        if not request.session.get('otp_verified'):
            return redirect('forgot_password')
            
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            email = request.session.get('reset_email')
            user = CustomUser.objects.get(email=email)
            user.set_password(password)
            user.save()
            
            # Clear session
            del request.session['reset_email']
            del request.session['otp_verified']
            
            messages.success(request, "Password reset successfully. You can now login.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
        return render(request, 'UserApp/reset_password.html')
from django.utils import timezone
from django.db.models import Q

class LandingPageView(TemplateView):
    template_name = 'UserApp/landing.html'

class AboutView(TemplateView):
    template_name = 'UserApp/about.html'

class ContactView(View):
    def get(self, request):
        return render(request, 'UserApp/contact.html')

    def post(self, request):
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')

        if full_name and email and subject and message_body:
            # Save message to DB
            ContactMessage.objects.create(
                full_name=full_name,
                email=email,
                subject=subject,
                message=message_body
            )

            # Send Thank You Email (Designed HTML)
            try:
                context = {
                    'full_name': full_name,
                    'subject': subject,
                    'message': message_body,
                }
                html_content = render_to_string('emails/contact_thanks.html', context)
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    subject=f"We received your message, {full_name}!",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'support@notesapp.com',
                    to=[email],
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=True)
            except Exception as e:
                print(f"Error sending email: {e}")

            messages.success(request, "Your message has been sent successfully! Check your email for a confirmation.")
            return redirect('contact')
        
        messages.error(request, "Please fill in all fields.")
        return render(request, 'UserApp/contact.html')

class BlogView(TemplateView):
    template_name = 'UserApp/blog.html'

class SignupView(CreateView):
    model = CustomUser
    form_class = SignupForm
    template_name = 'UserApp/signup.html'
    success_url = reverse_lazy('verify_otp')

    def form_valid(self, form):
        user = form.save()
        send_otp_email(user)
        self.request.session['unverified_user_email'] = user.email
        messages.success(self.request, "Account created! Please verify your email with the OTP sent.")
        return super().form_valid(form)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'UserApp/login.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.user_cache
        if not user.is_verified:
            send_otp_email(user)
            self.request.session['unverified_user_email'] = user.email
            messages.warning(self.request, "Please verify your email before logging in.")
            return redirect('verify_otp')
        
        login(self.request, user)
        return super().form_valid(form)

class VerifyOTPView(View):
    def get(self, request):
        email = request.session.get('unverified_user_email')
        if not email:
            return redirect('signup')
        return render(request, 'UserApp/verify_otp.html', {'email': email})

    def post(self, request):
        email = request.session.get('unverified_user_email')
        otp_code = request.POST.get('otp')
        
        user = get_object_or_404(CustomUser, email=email)
        otp = OTP.objects.filter(user=user).first()

        if otp and otp.code == otp_code:
            if otp.is_expired():
                messages.error(request, "OTP has expired. Please resend.")
                return redirect('verify_otp')
            
            user.is_verified = True
            user.save()
            otp.delete()
            if 'unverified_user_email' in request.session:
                del request.session['unverified_user_email']
            messages.success(request, "Email verified successfully! Please log in to continue.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')

class ResendOTPView(View):
    def get(self, request):
        email = request.session.get('unverified_user_email')
        if email:
            user = CustomUser.objects.filter(email=email).first()
            if user:
                send_otp_email(user)
                messages.success(request, "A new OTP has been sent to your email.")
        return redirect('verify_otp')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class DashboardView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'UserApp/dashboard.html'
    context_object_name = 'notes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        # Show all Approved notes (Community) OR user's own notes (even if pending)
        notes = Note.objects.filter(Q(status='Approved') | Q(user=self.request.user)).distinct().order_by('-created_at')
        if query:
            notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(user__full_name__icontains=query))
        return notes

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'UserApp/note_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Note created successfully!")
        return super().form_valid(form)

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'UserApp/note_form.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Note updated successfully!")
        return super().form_valid(form)

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'UserApp/note_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Note deleted successfully!")
        return super().delete(request, *args, **kwargs)

class DownloadNoteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        
        # Permission check: Owner or Staff
        if note.user != request.user and not request.user.is_staff:
            messages.error(request, "Access denied.")
            return redirect('dashboard')
            
        # Create text content
        content = f"TITLE: {note.title}\n"
        content += f"CATEGORY: {note.category}\n"
        content += f"CREATED BY: {note.user.full_name}\n"
        content += f"DATE: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"STATUS: {note.status}\n"
        content += "\n" + "="*30 + "\n\n"
        content += note.content
        
        # Create response
        response = HttpResponse(content, content_type='text/plain')
        filename = f"{note.title.replace(' ', '_')}.txt"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response

class NoteUpdateAJAXView(LoginRequiredMixin, View):
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        if note.user != request.user:
            return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)
        
        try:
            data = json.loads(request.body)
            note.title = data.get('title', note.title)
            note.content = data.get('content', note.content)
            note.category = data.get('category', note.category)
            # Reset status to Pending when edited for re-verification
            note.status = 'Pending'
            note.save()
            return JsonResponse({
                'success': True,
                'message': '✅ Note Updated Successfully!',
                'title': note.title,
                'content': note.content,
                'category': note.category,
                'status': note.status,
                'updated_at': note.updated_at.strftime('%b %d, %Y')
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

class ToggleSaveNoteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        if request.user in note.saved_by.all():
            note.saved_by.remove(request.user)
            saved = False
            message = "Note removed from saved collection"
        else:
            note.saved_by.add(request.user)
            saved = True
            message = "Note saved successfully!"
        
        return JsonResponse({
            'success': True,
            'saved': saved,
            'message': message
        })

class SavedNotesListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'UserApp/saved_notes.html'
    context_object_name = 'notes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        # Show notes saved by the user
        notes = self.request.user.saved_notes.all().order_by('-created_at')
        if query:
            notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(user__full_name__icontains=query))
        return notes

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'UserApp/profile.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)
