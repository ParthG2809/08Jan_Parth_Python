import googlemaps
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages

def index(request):
    result = None
    address = None
    error = None

    if request.method == "POST":
        address = request.POST.get('address')
        api_key = settings.GOOGLE_MAPS_API_KEY

        if not api_key:
            error = "Google Maps API Key is missing. Please add it to your .env file."
        elif address:
            try:
                gmaps = googlemaps.Client(key=api_key)
                # Geocoding an address
                geocode_result = gmaps.geocode(address)

                if geocode_result:
                    location = geocode_result[0]['geometry']['location']
                    formatted_address = geocode_result[0]['formatted_address']
                    result = {
                        'lat': location['lat'],
                        'lng': location['lng'],
                        'formatted_address': formatted_address,
                    }
                else:
                    error = "Could not find coordinates for this address. Please try a more specific address."
            except Exception as e:
                error = f"An error occurred: {str(e)}"
        else:
            error = "Please enter an address."

    return render(request, 'geocoder/index.html', {
        'result': result,
        'address': address,
        'error': error,
        'api_key_configured': bool(settings.GOOGLE_MAPS_API_KEY)
    })
