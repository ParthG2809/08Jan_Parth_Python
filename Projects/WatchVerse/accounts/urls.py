from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp_view, name='verify-otp'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('reset-password/', views.reset_password_view, name='reset-password'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profile & Social
    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:email>/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit-profile'),
    path('follow/<int:user_id>/', views.follow_user_view, name='follow-user'),

    # Cinematic Media Integration (Support hybrid string IDs)
    path('media/<str:media_id>/', views.media_detail_view, name='media-detail'),

    # Dynamic Complete Discovery & Multi-language Advanced Search
    path('search/', views.search_view, name='search'),
    path('search/api/', views.search_api_view, name='search-api'),
    path('explore/', views.explore_view, name='explore'),
]
