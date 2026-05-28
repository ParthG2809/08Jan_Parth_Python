from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm

def profile_list(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = UserProfileForm()

    profiles = UserProfile.objects.all()
    return render(request, 'profiles/profile_list.html', {
        'form': form,
        'profiles': profiles
    })
