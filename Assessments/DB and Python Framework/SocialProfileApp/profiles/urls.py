from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profile_list, name='list'),
    path('create/', views.profile_create, name='create'),
    path('edit/<int:pk>/', views.profile_edit, name='edit'),
    path('export/', views.profile_export, name='export'),
]
