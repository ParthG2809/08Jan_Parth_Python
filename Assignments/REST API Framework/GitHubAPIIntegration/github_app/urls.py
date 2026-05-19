from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list_repositories, name='list_repositories'),
    path('create/', views.create_repository, name='create_repository'),
    path('login/github/', views.github_login, name='github_login'),
    path('callback/', views.github_callback, name='github_callback'),
    path('logout/github/', views.github_logout, name='github_logout'),
]
