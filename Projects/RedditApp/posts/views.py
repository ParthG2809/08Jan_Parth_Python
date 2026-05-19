from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Post, Vote, PollOption, SavedPost, Report
from .forms import PostCreateForm

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('feed:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        # Handle Poll Options
        if form.cleaned_data['post_type'] == 'poll':
            options = form.cleaned_data['poll_options'].split('\n')
            for opt in options:
                if opt.strip():
                    PollOption.objects.create(post=self.object, text=opt.strip())
        return response

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        form.instance.is_edited = True
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('feed:home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class VoteView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        value = int(request.POST.get('value')) # 1 or -1
        
        vote, created = Vote.objects.get_or_create(user=request.user, post=post, defaults={'value': value})
        
        if not created:
            if vote.value == value:
                # Toggle vote off if clicking same button
                vote.delete()
                if value == 1: post.upvotes -= 1
                else: post.downvotes -= 1
            else:
                # Switch vote
                if value == 1:
                    post.upvotes += 1
                    post.downvotes -= 1
                else:
                    post.downvotes += 1
                    post.upvotes -= 1
                vote.value = value
                vote.save()
        else:
            if value == 1: post.upvotes += 1
            else: post.downvotes += 1
            
        post.save()
        return JsonResponse({'score': post.score, 'user_vote': value if not created or vote.value == value else 0})

class SocialActionView(LoginRequiredMixin, View):
    def post(self, request, post_id, action):
        post = get_object_or_404(Post, id=post_id)
        
        if action == 'save':
            obj, created = SavedPost.objects.get_or_create(user=request.user, post=post)
            if not created: obj.delete()
            return JsonResponse({'saved': created})
            
        elif action == 'report':
            reason = request.POST.get('reason')
            Report.objects.create(user=request.user, post=post, reason=reason)
            return JsonResponse({'reported': True})
            
        return JsonResponse({'error': 'Invalid action'}, status=400)
    
class PollVoteView(LoginRequiredMixin, View):
    def post(self, request, option_id):
        option = get_object_or_404(PollOption, id=option_id)
        option.vote_count += 1
        option.save()
        return JsonResponse({'votes': option.vote_count})
