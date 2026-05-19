from django.urls import path
from .views import (
    LandingPageView, SignupView, LoginView, VerifyOTPView, LogoutView,
    DashboardView, NoteCreateView, NoteUpdateView, NoteDeleteView, ResendOTPView,
    AboutView, ContactView, BlogView, DownloadNoteView, NoteUpdateAJAXView,
    ToggleSaveNoteView, SavedNotesListView, UserProfileView,
    ForgotPasswordView, VerifyOTPResetView, ResetPasswordView
)

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-otp-reset/', VerifyOTPResetView.as_view(), name='verify_otp_reset'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('note/<int:pk>/download/', DownloadNoteView.as_view(), name='note_download'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('note/new/', NoteCreateView.as_view(), name='note_create'),
    path('note/<int:pk>/edit/', NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/edit-ajax/', NoteUpdateAJAXView.as_view(), name='note_update_ajax'),
    path('note/<int:pk>/save-toggle/', ToggleSaveNoteView.as_view(), name='note_save_toggle'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
    path('saved-notes/', SavedNotesListView.as_view(), name='saved_notes'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
