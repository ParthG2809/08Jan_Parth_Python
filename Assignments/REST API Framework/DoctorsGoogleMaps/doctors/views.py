from django.shortcuts import render
from django.conf import settings
from .models import Doctor

def doctor_map(request):
    city_query = request.GET.get('city', '').strip()
    
    if city_query:
        doctors = Doctor.objects.filter(city__icontains=city_query)
    else:
        doctors = Doctor.objects.all()

    # Get distinct cities for a dropdown filter
    cities = Doctor.objects.values_list('city', flat=True).distinct()

    context = {
        'doctors': doctors,
        'cities': cities,
        'selected_city': city_query,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'doctors/map.html', context)
