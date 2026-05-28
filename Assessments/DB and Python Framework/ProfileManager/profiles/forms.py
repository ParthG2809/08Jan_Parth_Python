from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'age', 'is_public']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-700 bg-gray-900/50 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
                'placeholder': 'Enter username',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-700 bg-gray-900/50 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
                'placeholder': 'Enter age',
                'min': '0',
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded border-gray-700 text-purple-600 focus:ring-purple-500 bg-gray-900/50 focus:ring-offset-gray-950 transition duration-200 cursor-pointer',
            }),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age <= 13:
            raise forms.ValidationError("You must be over 13 years old to create a profile.")
        return age
