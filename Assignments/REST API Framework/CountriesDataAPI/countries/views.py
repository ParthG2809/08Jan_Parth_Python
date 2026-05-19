import requests
from django.shortcuts import render

def index(request):
    query = request.GET.get('q', '').strip()
    context = {'query': query}

    if query:
        url = f"https://restcountries.com/v3.1/name/{query}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    country_data = data[0]
                    context['country'] = {
                        'name': country_data.get('name', {}).get('common', 'N/A'),
                        'official_name': country_data.get('name', {}).get('official', 'N/A'),
                        'population': f"{country_data.get('population', 0):,}",
                        'languages': ', '.join(country_data.get('languages', {}).values()) if country_data.get('languages') else 'N/A',
                        'currencies': ', '.join([f"{c.get('name')} ({c.get('symbol', '')})" for c in country_data.get('currencies', {}).values()]) if country_data.get('currencies') else 'N/A',
                        'flag': country_data.get('flags', {}).get('svg') or country_data.get('flags', {}).get('png', ''),
                        'flag_alt': country_data.get('flags', {}).get('alt', ''),
                        'capital': ', '.join(country_data.get('capital', [])) if country_data.get('capital') else 'N/A',
                        'region': country_data.get('region', 'N/A'),
                        'subregion': country_data.get('subregion', 'N/A'),
                    }
            elif response.status_code == 404:
                context['error'] = 'Country not found. Please try another search.'
            else:
                context['error'] = 'Failed to fetch country data. Please try again later.'
        except requests.exceptions.RequestException:
            context['error'] = 'Network error occurred. Please try again later.'

    return render(request, 'countries/index.html', context)
