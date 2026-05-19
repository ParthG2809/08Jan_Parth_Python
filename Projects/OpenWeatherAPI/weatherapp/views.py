from django.shortcuts import render
import requests
from django.conf import settings
from datetime import datetime

def index(request):
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.POST.get('city')
        if city:
            api_key = settings.OPENWEATHER_API_KEY
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            
            try:
                response = requests.get(url)
                data = response.json()
                
                if response.status_code == 200:
                    weather_data = {
                        'city': data['name'],
                        'temperature': round(data['main']['temp']),
                        'description': data['weather'][0]['description'].capitalize(),
                        'icon': data['weather'][0]['icon'],
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'wind_deg': data['wind'].get('deg'),
                        'feels_like': round(data['main']['feels_like']),
                        'temp_min': round(data['main']['temp_min']),
                        'temp_max': round(data['main']['temp_max']),
                        'pressure': data['main']['pressure'],
                        'country': data['sys']['country'],
                        'lat': data['coord']['lat'],
                        'lon': data['coord']['lon'],
                        'visibility': round(data.get('visibility', 0) / 1000, 1),
                        'clouds': data['clouds']['all'],
                        'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p'),
                        'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p'),
                        'current_date': datetime.now().strftime('%A, %d %B %Y'),
                    }
                else:
                    error_message = f"City '{city}' not found. Please try again."
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"

    return render(request, 'weatherapp/index.html', {
        'weather_data': weather_data,
        'error_message': error_message
    })
