from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    POST_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('link', 'Link'),
        ('poll', 'Poll'),
    )

    title = models.CharField(max_length=300)
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text')
    content = models.TextField(blank=True, null=True) # For text posts
    media_file = models.FileField(upload_to='post_media/', blank=True, null=True) # For image/video
    link_url = models.URLField(blank=True, null=True) # For link posts
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='all_posts')
    community = models.ForeignKey('feed.Community', on_delete=models.CASCADE, related_name='all_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    @property
    def score(self):
        return self.upvotes - self.downvotes

    def __str__(self):
        return self.title

class PollOption(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='poll_options')
    text = models.CharField(max_length=200)
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_votes')
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')

class SavedPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class Report(models.Model):
    REASONS = (
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('hate', 'Hate Speech'),
        ('misinformation', 'Misinformation'),
        ('other', 'Other'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    reason = models.CharField(max_length=20, choices=REASONS)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
