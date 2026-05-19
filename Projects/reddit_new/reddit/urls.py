from django.contrib import admin
from django.urls import path, include
from reddit import views

urlpatterns = [
    path('', views.index),
]