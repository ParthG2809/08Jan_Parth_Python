from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    path('<int:post_id>/vote/', views.VoteView.as_view(), name='vote'),
    path('<int:post_id>/action/<str:action>/', views.SocialActionView.as_view(), name='action'),
    path('poll/vote/<int:option_id>/', views.PollVoteView.as_view(), name='poll_vote'),
]
