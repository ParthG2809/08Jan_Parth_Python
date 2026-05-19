from django.urls import path
from .views import (
    AdminLoginView, AdminDashboardView, AdminUserListView, 
    AdminToggleUserStatusView, AdminNoteListView, AdminNoteActionView,
    AdminPromoteUserView, AdminUserCreateView, AdminUserUpdateView, AdminUserDeleteView,
    AdminContactMessageListView, AdminContactMessageDeleteView,
    AdminContactMessageDetailView, AdminContactMessageReplyView
)

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin_login'),
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('users/', AdminUserListView.as_view(), name='admin_users'),
    path('users/add/', AdminUserCreateView.as_view(), name='admin_user_create'),
    path('users/<int:pk>/edit/', AdminUserUpdateView.as_view(), name='admin_user_update'),
    path('users/<int:pk>/delete/', AdminUserDeleteView.as_view(), name='admin_user_delete'),
    path('users/<int:pk>/toggle/', AdminToggleUserStatusView.as_view(), name='admin_toggle_user'),
    path('users/<int:pk>/promote/', AdminPromoteUserView.as_view(), name='admin_promote_user'),
    path('notes/', AdminNoteListView.as_view(), name='admin_notes'),
    path('notes/<int:pk>/<str:action>/', AdminNoteActionView.as_view(), name='admin_note_action'),
    path('contact-messages/', AdminContactMessageListView.as_view(), name='admin_contact_messages'),
    path('contact-messages/<int:pk>/', AdminContactMessageDetailView.as_view(), name='admin_contact_message_detail'),
    path('contact-messages/<int:pk>/reply/', AdminContactMessageReplyView.as_view(), name='admin_contact_message_reply'),
    path('contact-messages/<int:pk>/delete/', AdminContactMessageDeleteView.as_view(), name='admin_contact_message_delete'),
]
