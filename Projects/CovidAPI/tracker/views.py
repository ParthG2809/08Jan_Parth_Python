import requests
from django.shortcuts import render

def index(request):
    url = "https://api.rootnet.in/covid19-in/stats/latest"
    response = requests.get(url)
    data = response.json()
    
    # Extracting the required information
    last_updated = data.get('lastOriginUpdate')
    summary = data.get('data', {}).get('summary', {})
    regional = data.get('data', {}).get('regional', [])
    
    context = {
        'summary': summary,
        'regional': regional,
        'last_updated': last_updated
    }
    return render(request, 'tracker/index.html', context)
