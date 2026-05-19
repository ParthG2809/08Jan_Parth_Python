from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet

# Register our viewset routes with the DefaultRouter
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')

urlpatterns = [
    path('', include(router.urls)),
]
