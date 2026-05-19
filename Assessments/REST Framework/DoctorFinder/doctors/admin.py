from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialization', 'city')
    list_filter = ('specialization', 'city')
    search_fields = ('name', 'specialization', 'city')
