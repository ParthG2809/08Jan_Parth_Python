from django.db import models
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.db.models import Q
from .models import Community
from posts.models import Post
from .utils import sort_posts

class HomeFeedView(ListView):
    model = Post
    template_name = 'feed/home_feed.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        sort_type = self.request.GET.get('sort', 'hot')
        
        if self.request.user.is_authenticated:
            # Personalized: Joined communities
            joined_communities = self.request.user.joined_communities.all()
            if joined_communities.exists():
                queryset = Post.objects.filter(community__in=joined_communities)
            else:
                queryset = Post.objects.all()
        else:
            queryset = Post.objects.all()
            
        return sort_posts(queryset, sort_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'hot')
        context['trending_communities'] = Community.objects.all()[:5] # Placeholder for trends
        return context

class PostListAPIView(View):
    """
    API for infinite scroll returning JSON
    """
    def get(self, request, *args, **kwargs):
        page = int(request.GET.get('page', 1))
        sort_type = request.GET.get('sort', 'hot')
        limit = 10
        offset = (page - 1) * limit
        
        queryset = Post.objects.all() # Simplify for API example
        posts = sort_posts(queryset, sort_type)[offset:offset+limit]
        
        data = []
        for post in posts:
            data.append({
                'id': post.id,
                'title': post.title,
                'content': post.content[:200] + '...',
                'author': post.author.username,
                'community': post.community.name,
                'score': post.score,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M'),
                'image_url': post.media_file.url if post.media_file and post.post_type == 'image' else None,
            })
            
        return JsonResponse({'posts': data, 'has_next': len(data) == limit})
