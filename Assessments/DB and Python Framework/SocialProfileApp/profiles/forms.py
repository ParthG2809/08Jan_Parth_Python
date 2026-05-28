from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone', 'occupation', 'location', 'bio']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. John',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Doe',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. john.doe@example.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. +1 (555) 019-2834',
            }),
            'occupation': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Software Architect',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. San Francisco, CA',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Tell us a bit about yourself, your interests, and achievements...',
                'rows': 4,
            }),
        }
