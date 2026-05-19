from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, FormView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib import messages
from UserApp.models import CustomUser, Note
from .models import ContactMessage
from UserApp.forms import LoginForm
from UserApp.utils import send_note_status_email
from django import forms
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import JsonResponse

class AdminUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=False, help_text="Leave blank to keep current password")
    
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'mobile_number', 'city', 'is_verified', 'is_active', 'is_staff']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 dark:bg-zinc-800 border rounded-2xl focus:ring-1 focus:ring-black outline-none dark:text-white'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-4 bg-gray-50 dark:bg-zinc-800 border rounded-2xl focus:ring-1 focus:ring-black outline-none dark:text-white'}),
            'mobile_number': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 dark:bg-zinc-800 border rounded-2xl focus:ring-1 focus:ring-black outline-none dark:text-white'}),
            'city': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 dark:bg-zinc-800 border rounded-2xl focus:ring-1 focus:ring-black outline-none dark:text-white'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class AdminStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class AdminLoginView(FormView):
    template_name = 'AdminApp/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('admin_dashboard')

    def form_valid(self, form):
        user = form.user_cache
        if user.is_staff:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Access denied. Not an admin.")
            return redirect('admin_login')

class AdminDashboardView(AdminStaffRequiredMixin, TemplateView):
    template_name = 'AdminApp/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = CustomUser.objects.count()
        context['verified_users'] = CustomUser.objects.filter(is_verified=True).count()
        context['total_notes'] = Note.objects.count()
        context['pending_notes'] = Note.objects.filter(status='Pending').count()
        context['unread_messages'] = ContactMessage.objects.filter(is_read=False).count()
        context['total_messages'] = ContactMessage.objects.count()
        context['recent_users'] = CustomUser.objects.order_by('-date_joined')[:5]
        return context

class AdminUserListView(AdminStaffRequiredMixin, ListView):
    model = CustomUser
    template_name = 'AdminApp/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date_joined')
        tab = self.request.GET.get('tab', 'all')
        
        if tab == 'verified':
            queryset = queryset.filter(is_verified=True)
        elif tab == 'blocked':
            queryset = queryset.filter(is_active=False)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_tab'] = self.request.GET.get('tab', 'all')
        return context

class AdminUserCreateView(AdminStaffRequiredMixin, CreateView):
    model = CustomUser
    form_class = AdminUserForm
    template_name = 'AdminApp/user_form.html'
    success_url = reverse_lazy('admin_users')

    def form_valid(self, form):
        messages.success(self.request, f"User {form.instance.email} created successfully.")
        return super().form_valid(form)

class AdminUserUpdateView(AdminStaffRequiredMixin, UpdateView):
    model = CustomUser
    form_class = AdminUserForm
    template_name = 'AdminApp/user_form.html'
    success_url = reverse_lazy('admin_users')

    def form_valid(self, form):
        messages.success(self.request, f"User {form.instance.email} updated successfully.")
        return super().form_valid(form)

class AdminUserDeleteView(AdminStaffRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'AdminApp/user_confirm_delete.html'
    success_url = reverse_lazy('admin_users')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            messages.error(request, "You cannot delete yourself!")
            return redirect('admin_users')
        messages.success(self.request, f"User {user.email} deleted successfully.")
        return super().delete(request, *args, **kwargs)

from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

class AdminContactMessageListView(AdminStaffRequiredMixin, ListView):
    model = ContactMessage
    template_name = 'AdminApp/contact_messages.html'
    context_object_name = 'contact_messages'
    paginate_by = 10
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_count'] = ContactMessage.objects.filter(is_read=False).count()
        return context

class AdminContactMessageDetailView(AdminStaffRequiredMixin, View):
    def get(self, request, pk):
        message = get_object_or_404(ContactMessage, pk=pk)
        if not message.is_read:
            message.is_read = True
            message.save()
        
        return JsonResponse({
            'id': message.id,
            'full_name': message.full_name,
            'email': message.email,
            'subject': message.subject,
            'message': message.message,
            'created_at': message.created_at.strftime("%b %d, %Y %H:%M"),
        })

class AdminContactMessageReplyView(AdminStaffRequiredMixin, View):
    def post(self, request, pk):
        message = get_object_or_404(ContactMessage, pk=pk)
        reply_body = request.POST.get('reply_body')
        
        if reply_body:
            try:
                context = {
                    'full_name': message.full_name,
                    'subject': message.subject,
                    'reply_body': reply_body,
                    'original_message': message.message,
                }
                html_content = render_to_string('emails/admin_reply.html', context)
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    subject=f"Re: {message.subject}",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[message.email],
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)
                
                messages.success(request, f"Reply sent to {message.email}")
            except Exception as e:
                messages.error(request, f"Error sending email: {e}")
        
        return redirect('admin_contact_messages')

class AdminContactMessageDeleteView(AdminStaffRequiredMixin, DeleteView):
    model = ContactMessage
    success_url = reverse_lazy('admin_contact_messages')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Message deleted successfully.")
        return super().delete(request, *args, **kwargs)

class AdminToggleUserStatusView(AdminStaffRequiredMixin, View):
    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        if user == request.user:
            messages.error(request, "You cannot deactivate yourself!")
        else:
            user.is_active = not user.is_active
            user.save()
            status = "activated" if user.is_active else "deactivated"
            messages.success(request, f"User {user.email} has been {status}.")
        return redirect('admin_users')

class AdminPromoteUserView(AdminStaffRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        if user == request.user:
            messages.warning(request, "You are already an admin.")
        else:
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request, f"User {user.email} is now a superuser and administrator.")
        return redirect('admin_users')

class AdminNoteListView(AdminStaffRequiredMixin, ListView):
    model = Note
    template_name = 'AdminApp/note_list.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        status = self.request.GET.get('status', 'Pending')
        return Note.objects.filter(status=status).order_by('-created_at')

class AdminNoteActionView(AdminStaffRequiredMixin, View):
    def post(self, request, pk, action):
        note = get_object_or_404(Note, pk=pk)
        if action == 'approve':
            note.status = 'Approved'
        elif action == 'reject':
            note.status = 'Rejected'
        
        note.save()
        send_note_status_email(note)
        messages.success(request, f"Note has been {note.status} and user notified.")
        return redirect('admin_notes')
