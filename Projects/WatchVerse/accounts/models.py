from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp

class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class MediaItem(models.Model):
    MEDIA_TYPES = (
        ('MOVIE', 'Movie'),
        ('SERIES', 'Series'),
        ('ANIME', 'Anime'),
    )
    VERDICT_CHOICES = (
        ('SKIP', 'Skip'),
        ('OTW', 'One-Time Watch'),
        ('WW', 'Worth Watching'),
        ('PEAK', 'Peak'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    backdrop = models.ImageField(upload_to='backdrops/', blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    rating_avg = models.FloatField(default=0.0)
    verdict = models.CharField(max_length=10, choices=VERDICT_CHOICES, default='WW')
    genres = models.ManyToManyField(Genre, related_name='media_items', blank=True)
    is_featured = models.BooleanField(default=False)
    is_hidden_gem = models.BooleanField(default=False)

    # TMDB Integration
    tmdb_id = models.IntegerField(null=True, blank=True)
    tmdb_poster_path = models.CharField(max_length=255, null=True, blank=True)
    tmdb_backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    
    # External Ratings
    imdb_id = models.CharField(max_length=20, null=True, blank=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    rt_rating = models.IntegerField(null=True, blank=True) # Percentage

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def get_poster_url(self):
        if self.poster:
            return self.poster.url
        if self.tmdb_poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.tmdb_poster_path}"
        return None

    @property
    def get_backdrop_url(self):
        if self.backdrop:
            return self.backdrop.url
        if self.tmdb_backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.tmdb_backdrop_path}"
        return None

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    favorite_genres = models.CharField(max_length=255, blank=True) # Comma separated
    is_public = models.BooleanField(default=True)
    
    # Favorites & Watchlist (M2M)
    favorites = models.ManyToManyField(MediaItem, related_name='favorited_by', blank=True)
    watchlist = models.ManyToManyField(MediaItem, related_name='watchlisted_by', blank=True)

    def __str__(self):
        return f"{self.user.full_name}'s Profile"

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Review(models.Model):
    VERDICT_CHOICES = (
        ('SKIP', 'Skip'),
        ('OTW', 'One-Time Watch'),
        ('WW', 'Worth Watching'),
        ('PEAK', 'Peak'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField() # 1-10
    verdict = models.CharField(max_length=10, choices=VERDICT_CHOICES, default='WW')
    comment = models.TextField()
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE)
    progress_percent = models.IntegerField(default=0)
    last_watched = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'media_item')
        ordering = ['-last_watched']

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    items = models.ManyToManyField(MediaItem, related_name='collections')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Activity(models.Model):
    TYPES = (
        ('REVIEW', 'Review'),
        ('FAVORITE', 'Favorite'),
        ('WATCHLIST', 'Watchlist'),
        ('FOLLOW', 'Follow'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=TYPES)
    content_object_id = models.IntegerField(null=True, blank=True) # Generic reference ID
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)
