import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WatchVerse.settings')
django.setup()

from accounts.models import MediaItem, Genre

def mock_sync():
    data = [
        {
            "title": "Dune: Part Two",
            "media_type": "MOVIE",
            "release_year": 2024,
            "description": "Follow the mythic journey of Paul Atreides as he unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family.",
            "rating_avg": 8.3,
            "tmdb_poster_path": "/1pdf3ZHLW0zkJa9qGvUvS9nUKr8.jpg",
            "tmdb_backdrop_path": "/xOMo8NETs_wVda61p6vI93vYpZf.jpg",
            "verdict": "PEAK",
            "genres": ["Sci-Fi", "Adventure"],
            "is_featured": True
        },
        {
            "title": "Oppenheimer",
            "media_type": "MOVIE",
            "release_year": 2023,
            "description": "The story of J. Robert Oppenheimer's role in the development of the atomic bomb during World War II.",
            "rating_avg": 8.1,
            "tmdb_poster_path": "/8GxvynZTMBLSqs9zGk78GjSbe0m.jpg",
            "tmdb_backdrop_path": "/fm6Np0Y80QkdAF3S7vi9MRqIDLp.jpg",
            "verdict": "PEAK",
            "genres": ["Drama", "History"]
        },
        {
            "title": "Cyberpunk: Edgerunners",
            "media_type": "ANIME",
            "release_year": 2022,
            "description": "In a dystopia riddled with corruption and cybernetic implants, a talented but reckless street kid strives to become a mercenary outlaw — an edgerunner.",
            "rating_avg": 8.6,
            "tmdb_poster_path": "/799799-Cyberpunk-Edgerunners.jpg", # Note: using paths that exist or look real
            "tmdb_poster_path": "/766766-Edgerunners.jpg",
            "tmdb_backdrop_path": "/667788-NightCity.jpg",
            "verdict": "PEAK",
            "genres": ["Anime", "Action", "Sci-Fi"]
        },
        {
            "title": "The Last of Us",
            "media_type": "SERIES",
            "release_year": 2023,
            "description": "After a global pandemic destroys civilization, a hardened survivor takes charge of a 14-year-old girl who may be humanity's last hope.",
            "rating_avg": 8.7,
            "tmdb_poster_path": "/u3YvH2oqM2ij3qrIsS06vI3uHia.jpg",
            "tmdb_backdrop_path": "/uDgyAhy59yogHUnY75r06jGjueR.jpg",
            "verdict": "WW",
            "genres": ["Drama", "Action"]
        },
        {
            "title": "Shogun",
            "media_type": "SERIES",
            "release_year": 2024,
            "description": "When a mysterious European ship is found abandoned in a nearby fishing village, Lord Yoshii Toranaga discovers secrets that could tip the scales of power.",
            "rating_avg": 8.5,
            "tmdb_poster_path": "/7O4SpgBNI7EzZ0R9pX9IUA9oOno.jpg",
            "tmdb_backdrop_path": "/566778-Shogun.jpg",
            "verdict": "PEAK",
            "genres": ["Drama", "History"]
        }
    ]

    for item_data in data:
        media_item, created = MediaItem.objects.get_or_create(
            title=item_data['title'],
            defaults={
                'media_type': item_data['media_type'],
                'release_year': item_data['release_year'],
                'description': item_data['description'],
                'rating_avg': item_data['rating_avg'],
                'tmdb_poster_path': item_data['tmdb_poster_path'],
                'tmdb_backdrop_path': item_data['tmdb_backdrop_path'],
                'verdict': item_data['verdict'],
                'is_featured': item_data.get('is_featured', False)
            }
        )
        
        for g_name in item_data['genres']:
            genre, _ = Genre.objects.get_or_create(name=g_name)
            media_item.genres.add(genre)
        
        media_item.save()
        print(f"Synced: {media_item.title}")

if __name__ == "__main__":
    mock_sync()
