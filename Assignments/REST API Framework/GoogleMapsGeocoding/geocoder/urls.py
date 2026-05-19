from django.urls import path
from . import views

app_name = 'geocoder'

urlpatterns = [
    path('', views.index, name='index'),
]
