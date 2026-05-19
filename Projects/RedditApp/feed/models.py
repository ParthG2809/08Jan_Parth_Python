from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Sum

class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='community_icons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_communities', blank=True)

    def __str__(self):
        return f"r/{self.name}"
