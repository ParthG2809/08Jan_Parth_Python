from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from .models import Doctor
from .serializers import DoctorSerializer

class StandardLimitOffsetPagination(LimitOffsetPagination):
    """
    Standard pagination class implementing LimitOffsetPagination with safety limits.
    """
    default_limit = 10
    max_limit = 100
    limit_query_param = 'limit'
    offset_query_param = 'offset'

class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Doctor profiles.
    Provides standard endpoints (GET, POST, PUT, PATCH, DELETE) with atomic database
    safety, limit-offset pagination, and client-side sorting/filtering.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    pagination_class = StandardLimitOffsetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    # Client-side sorting fields
    ordering_fields = ['name', 'specialization', 'experience_years', 'consultation_fee', 'created_at']
    ordering = ['-created_at']  # Default sorting: newly registered doctors first

    # Client-side text-based search
    search_fields = ['name', 'specialization']

    def create(self, request, *args, **kwargs):
        """
        Create a Doctor profile. Operation wrapped in transaction.atomic to ensure database safety.
        """
        with transaction.atomic():
            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Fully update a Doctor profile. Operation wrapped in transaction.atomic to ensure database safety.
        """
        with transaction.atomic():
            return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a Doctor profile. Operation wrapped in transaction.atomic to ensure database safety.
        """
        with transaction.atomic():
            return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a Doctor profile. Operation wrapped in transaction.atomic to ensure database safety.
        """
        with transaction.atomic():
            return super().destroy(request, *args, **kwargs)
