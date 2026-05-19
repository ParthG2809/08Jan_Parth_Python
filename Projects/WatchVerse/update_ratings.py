import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WatchVerse.settings')
django.setup()

from accounts.models import MediaItem
from django.conf import settings

def update_ratings():
    items = MediaItem.objects.all()
    print(f"Updating ratings for {items.count()} items.")
    
    for item in items:
        # Simulate ratings based on TMDB score if not already present
        base_score = float(item.rating_avg or 0.0)
        if base_score > 0:
            item.imdb_rating = round(base_score - 0.2, 1)
            item.rt_rating = int(base_score * 10 + (base_score * 0.5))
            if item.rt_rating > 98: item.rt_rating = 98
            
            # Ensure some variety
            import random
            item.imdb_rating += random.choice([-0.1, 0, 0.1, 0.2])
            item.rt_rating += random.randint(-2, 5)
            if item.rt_rating > 100: item.rt_rating = 100
            
            item.save()
            print(f"Updated {item.title}: IMDb {item.imdb_rating}, RT {item.rt_rating}%")

if __name__ == "__main__":
    update_ratings()
