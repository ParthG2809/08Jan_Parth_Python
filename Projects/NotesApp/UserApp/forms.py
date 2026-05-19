from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser, Note

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'mobile_number', 'city', 'password']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")
            # We will check is_verified in the view
            self.user_cache = user
        return self.cleaned_data

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'file_upload']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Note Title', 'class': 'w-full p-3 border rounded-xl focus:ring-1 focus:ring-black outline-none'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write description here...', 'class': 'w-full p-3 border rounded-xl focus:ring-1 focus:ring-black outline-none', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'w-full p-3 border rounded-xl focus:ring-1 focus:ring-black outline-none'}),
            'file_upload': forms.FileInput(attrs={'class': 'w-full p-3 border border-dashed rounded-xl focus:ring-1 focus:ring-black outline-none'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'mobile_number', 'city', 'profile_photo']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 dark:bg-zinc-800 border rounded-2xl focus:ring-1 focus:ring-black outline-none dark:text-white'}),
            'mobile_number': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 dark:bg-zinc-800 border rounded-2xl focus:ring-1 focus:ring-black outline-none dark:text-white'}),
            'city': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 dark:bg-zinc-800 border rounded-2xl focus:ring-1 focus:ring-black outline-none dark:text-white'}),
            'profile_photo': forms.FileInput(attrs={'class': 'w-full p-4 bg-gray-50 dark:bg-zinc-800 border rounded-2xl focus:ring-1 focus:ring-black outline-none dark:text-white'}),
        }
