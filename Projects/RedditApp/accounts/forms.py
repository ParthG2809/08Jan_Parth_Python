from django.db import models
from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
        'placeholder': 'Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['email', 'username', 'fullname', 'mobile', 'city']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
                'placeholder': 'Email Address'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
                'placeholder': 'Username'
            }),
            'fullname': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
                'placeholder': 'Full Name'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
                'placeholder': 'Mobile Number'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
                'placeholder': 'City'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class OTPVerifyForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-3xl font-bold tracking-widest text-center transition duration-200',
        'placeholder': '· · · · · ·'
    }))

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
        'placeholder': 'Email Address'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 border-transparent focus:border-orange-500 focus:bg-white dark:focus:bg-gray-700 focus:ring-0 text-sm font-medium transition duration-200',
        'placeholder': 'Password'
    }))
