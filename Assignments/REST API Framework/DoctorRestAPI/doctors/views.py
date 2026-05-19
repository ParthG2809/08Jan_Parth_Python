from django.shortcuts import render
from rest_framework import viewsets
from .models import Doctor
from .serializers import DoctorSerializer

# Create your views here.

class DoctorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing doctor instances.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

def dashboard(request):
    """
    Serves the premium doctor management dashboard.
    """
    return render(request, 'doctors/index.html')
