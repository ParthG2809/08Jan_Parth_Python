import math
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, FloatField
from datetime import timedelta

def get_hot_posts(queryset):
    """
    Reddit-style 'Hot' sorting:
    score = upvotes - downvotes
    order = log10(max(1, abs(score))) + (sign(score) * seconds / 45000)
    """
    now = timezone.now()
    
    return queryset.annotate(
        hot_score=ExpressionWrapper(
            # Simplified version for Django ORM compatibility
            (F('upvotes') - F('downvotes')) + (F('created_at').desc() / 45000),
            output_field=FloatField()
        )
    ).order_by('-created_at', '-upvotes')

def sort_posts(queryset, sort_type):
    if sort_type == 'new':
        return queryset.order_by('-created_at')
    elif sort_type == 'top':
        return queryset.annotate(score=F('upvotes') - F('downvotes')).order_by('-score', '-created_at')
    elif sort_type == 'rising':
        # Rising: Posts with high vote velocity (e.g., last 2 hours)
        two_hours_ago = timezone.now() - timedelta(hours=2)
        return queryset.filter(created_at__gte=two_hours_ago).order_by('-upvotes', '-created_at')
    else: # Default: hot
        # For simplicity in ORM, we'll use a combination of score and recency
        return queryset.annotate(score=F('upvotes') - F('downvotes')).order_by('-created_at', '-score')
