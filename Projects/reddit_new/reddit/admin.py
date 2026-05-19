from django.contrib import admin
from .models import *

# Register your models here.
class UserData(admin.ModelAdmin):
    ordering=["id"]
    list_display=['id', 'name', 'email', 'username']

admin.site.register(Userinfo, UserData)