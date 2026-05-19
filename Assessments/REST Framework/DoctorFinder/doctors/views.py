from django.db import transaction
from rest_framework import viewsets
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def perform_create(self, serializer):
        # Wrap creation logic in an atomic transaction block
        with transaction.atomic():
            serializer.save()
