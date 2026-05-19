import os
import django
import random
from django.utils import timezone
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WatchVerse.settings')
django.setup()

from accounts.models import User, MediaItem, Genre, Review, Discussion, Collection, Profile

def populate():
    # 1. Create Genres
    genres_list = ['Action', 'Horror', 'Anime', 'Romance', 'Sci-Fi', 'Thriller', 'Drama', 'Adventure']
    genres = {}
    for g_name in genres_list:
        g, _ = Genre.objects.get_or_create(name=g_name, slug=slugify(g_name))
        genres[g_name] = g

    # 2. Create Media Items
    media_data = [
        {
            'title': 'Dune: Part Two',
            'type': 'MOVIE',
            'verdict': 'PEAK',
            'featured': True,
            'description': 'Paul Atreides unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family.',
            'genres': ['Action', 'Sci-Fi'],
            'year': 2024,
            'rating': 9.2
        },
        {
            'title': 'Cyberpunk: Edgerunners',
            'type': 'ANIME',
            'verdict': 'PEAK',
            'featured': False,
            'description': 'A street kid trying to survive in a technology and body modification-obsessed city of the future.',
            'genres': ['Anime', 'Sci-Fi', 'Action'],
            'year': 2022,
            'rating': 8.9
        },
        {
            'title': 'The Dark Knight',
            'type': 'MOVIE',
            'verdict': 'PEAK',
            'featured': False,
            'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
            'genres': ['Action', 'Thriller'],
            'year': 2008,
            'rating': 9.0
        },
        {
            'title': 'The Bear',
            'type': 'SERIES',
            'verdict': 'WW',
            'featured': False,
            'description': 'A young chef from the fine dining world comes home to Chicago to run his family sandwich shop.',
            'genres': ['Drama'],
            'year': 2022,
            'rating': 8.6
        },
        {
            'title': 'Shutter Island',
            'type': 'MOVIE',
            'verdict': 'WW',
            'featured': False,
            'description': 'In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.',
            'genres': ['Thriller', 'Horror'],
            'year': 2010,
            'rating': 8.2
        },
        {
            'title': 'Perfect Blue',
            'type': 'ANIME',
            'verdict': 'PEAK',
            'featured': False,
            'gem': True,
            'description': 'A retired pop idol turned actress begins to lose her grip on reality when she is stalked by an obsessed fan.',
            'genres': ['Anime', 'Thriller', 'Horror'],
            'year': 1997,
            'rating': 8.0
        }
    ]

    for data in media_data:
        m, created = MediaItem.objects.get_or_create(
            title=data['title'],
            media_type=data['type'],
            defaults={
                'description': data['description'],
                'verdict': data['verdict'],
                'is_featured': data.get('featured', False),
                'is_hidden_gem': data.get('gem', False),
                'release_year': data['year'],
                'rating_avg': data['rating']
            }
        )
        if created:
            for g_name in data['genres']:
                m.genres.add(genres[g_name])
            print(f"Created {m.title}")

    # 3. Create Discussions
    disc_data = [
        {'title': 'Best anime endings?', 'content': 'For me it has to be Code Geass. What about you guys?'},
        {'title': 'Most heartbreaking movie?', 'content': 'Grave of the Fireflies destroyed me.'},
        {'title': 'Peak Christopher Nolan film?', 'content': 'Inception vs Interstellar vs TDK. FIGHT!'}
    ]
    user = User.objects.first()
    if user:
        for d in disc_data:
            Discussion.objects.get_or_create(user=user, title=d['title'], content=d['content'])

    # 4. Create Collections
    collections = [
        {'title': 'Best Sci-Fi Movies', 'items': ['Dune: Part Two', 'Cyberpunk: Edgerunners']},
        {'title': 'Saddest Movies Ever', 'items': ['Perfect Blue']}
    ]
    if user:
        for c_data in collections:
            c, _ = Collection.objects.get_or_create(user=user, title=c_data['title'])
            for item_title in c_data['items']:
                item = MediaItem.objects.filter(title=item_title).first()
                if item:
                    c.items.add(item)

if __name__ == '__main__':
    populate()
