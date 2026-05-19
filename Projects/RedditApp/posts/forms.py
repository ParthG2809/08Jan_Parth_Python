from django import forms
from .models import Post, PollOption

class PostCreateForm(forms.ModelForm):
    poll_options = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter poll options (one per line)',
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
            'rows': 3
        }),
        required=False,
        help_text="Only for Poll posts"
    )

    class Meta:
        model = Post
        fields = ['title', 'post_type', 'community', 'content', 'media_file', 'link_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
                'placeholder': 'Title'
            }),
            'post_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
            }),
            'community': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
                'placeholder': 'Text (optional)',
                'rows': 5
            }),
            'link_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
                'placeholder': 'URL'
            }),
            'media_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
            }),
        }
