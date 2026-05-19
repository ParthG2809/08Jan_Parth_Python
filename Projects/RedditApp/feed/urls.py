from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.HomeFeedView.as_view(), name='home'),
    path('api/posts/', views.PostListAPIView.as_view(), name='post_api'),
]
