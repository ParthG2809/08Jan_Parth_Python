from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('payment/<int:appointment_id>/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
]
