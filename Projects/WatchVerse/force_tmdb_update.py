import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WatchVerse.settings')
django.setup()

from accounts.models import MediaItem, Genre
from django.conf import settings

def force_update_tmdb():
    items = MediaItem.objects.all()
    print(f"Found {items.count()} items to update.")
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}"
    }

    for item in items:
        print(f"Updating: {item.title}...")
        # Search for the item on TMDB
        search_type = "movie" if item.media_type == "MOVIE" else "tv"
        search_url = f"https://api.themoviedb.org/3/search/{search_type}?query={item.title}"
        
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                tmdb_data = results[0] # Take the first match
                item.tmdb_id = tmdb_data.get('id')
                item.description = tmdb_data.get('overview', '')
                item.rating_avg = tmdb_data.get('vote_average', 0.0)
                item.tmdb_poster_path = tmdb_data.get('poster_path')
                item.tmdb_backdrop_path = tmdb_data.get('backdrop_path')
                
                # Get more details for genres
                details_url = f"https://api.themoviedb.org/3/{search_type}/{item.tmdb_id}"
                details_resp = requests.get(details_url, headers=headers)
                if details_resp.status_code == 200:
                    details_data = details_resp.json()
                    for g_data in details_data.get('genres', []):
                        genre, _ = Genre.objects.get_or_create(name=g_data['name'])
                        item.genres.add(genre)
                
                item.save()
                print(f"Successfully updated {item.title} with TMDB ID {item.tmdb_id}")
            else:
                print(f"No TMDB results for {item.title}")
        else:
            print(f"Failed to connect to TMDB for {item.title}: {response.status_code}")

if __name__ == "__main__":
    force_update_tmdb()
