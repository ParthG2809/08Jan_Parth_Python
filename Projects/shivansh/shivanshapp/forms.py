from django import forms
from .models import * 

class studform(forms.ModelForm):
    class Meta:
        model = shivu
        fields='__all__'