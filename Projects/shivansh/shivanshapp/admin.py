from django.contrib import admin
from .models import *


# Register your models here.
class s(admin.ModelAdmin):
    ordering=["id"]
    list_display=["id","name","email"]

admin.site.register(shivu,s)