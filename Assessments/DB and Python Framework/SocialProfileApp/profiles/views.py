import csv
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm

def profile_list(request):
    """
    Dashboard view showing all profiles, search capabilities, and statistical highlights.
    """
    query = request.GET.get('q', '').strip()
    if query:
        profiles = Profile.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(location__icontains=query) |
            Q(occupation__icontains=query)
        ).order_by('-created_at')
    else:
        profiles = Profile.objects.all().order_by('-created_at')

    # Calculate statistics for the dashboard header cards
    total_count = Profile.objects.count()
    
    # Unique locations count, filtering out null/empty values
    locations = Profile.objects.exclude(location__isnull=True).exclude(location='').values_list('location', flat=True)
    unique_locations = len(set(locations))
    
    # Unique occupations count, filtering out null/empty values
    occupations = Profile.objects.exclude(occupation__isnull=True).exclude(occupation='').values_list('occupation', flat=True)
    unique_occupations = len(set(occupations))

    context = {
        'profiles': profiles,
        'query': query,
        'total_count': total_count,
        'unique_locations': unique_locations,
        'unique_occupations': unique_occupations,
    }
    return render(request, 'profiles/profile_list.html', context)

def profile_create(request):
    """
    Create a new profile using ProfileForm.
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save()
            messages.success(request, f"Profile for {profile} has been successfully created!")
            return redirect('profiles:list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm()
    
    return render(request, 'profiles/profile_form.html', {
        'form': form,
        'title': 'Create Profile',
        'is_edit': False
    })

def profile_edit(request, pk):
    """
    Edit an existing profile using ProfileForm.
    """
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"Profile for {profile} has been successfully updated!")
            return redirect('profiles:list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'profiles/profile_form.html', {
        'form': form,
        'title': 'Edit Profile',
        'is_edit': True,
        'profile': profile
    })

def profile_export(request):
    """
    Exports all database profile records into a downloadable CSV file.
    Uses Python's context manager (with open(...) as file:) for safe file operation.
    """
    # Define exports directory in the workspace
    exports_dir = os.path.join(settings.BASE_DIR, 'exports')
    os.makedirs(exports_dir, exist_ok=True)
    
    file_path = os.path.join(exports_dir, 'profiles_export.csv')
    
    # Fetch profiles to write
    profiles = Profile.objects.all().order_by('-created_at')
    
    # Write data to the CSV file using context manager
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write CSV Header
        writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Occupation', 'Location', 'Bio', 'Created At'])
        
        # Write Database Records
        for profile in profiles:
            writer.writerow([
                profile.id,
                profile.first_name,
                profile.last_name,
                profile.email,
                profile.phone or '',
                profile.occupation or '',
                profile.location or '',
                profile.bio or '',
                profile.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
            
    # Serve the file as a downloadable response
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename='profiles_export.csv')
        return response
    else:
        raise Http404("Export file could not be generated.")
