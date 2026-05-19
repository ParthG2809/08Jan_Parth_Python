from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, dashboard

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('api/', include(router.urls)),
]
