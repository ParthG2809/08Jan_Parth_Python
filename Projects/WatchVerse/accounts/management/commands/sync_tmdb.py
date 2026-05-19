from django.core.management.base import BaseCommand
from accounts.tmdb_utils import TMDBHelper
from accounts.models import MediaItem

class Command(BaseCommand):
    help = 'Sync trending content from TMDB'

    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, default=3, help='Number of pages to sync')

    def handle(self, *args, **options):
        pages = options['pages']
        
        types = [
            ("movie", "Movie"),
            ("tv", "Series")
        ]

        for m_type_key, m_type_label in types:
            self.stdout.write(self.style.NOTICE(f"\nFetching {m_type_label}s (Pages 1-{pages})..."))
            
            for page in range(1, pages + 1):
                self.stdout.write(f"Page {page}...")
                # We need to update TMDBHelper.fetch_trending to support page
                url = f"https://api.themoviedb.org/3/trending/{m_type_key}/day?page={page}"
                from django.conf import settings
                import requests
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}"
                }
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    continue
                
                results = response.json().get('results', [])
                for data in results:
                    # Fetch full details to get genres
                    details = TMDBHelper.fetch_details(data['id'], media_type=m_type_key)
                    if details:
                        item = TMDBHelper.sync_to_db(details, media_type=m_type_key)
                        item.tmdb_id = data['id']
                        
                        # Set dynamic verdicts
                        score = data.get('vote_average', 0)
                        if score >= 8.0:
                            item.verdict = 'PEAK'
                            item.is_featured = (page == 1 and data == results[0])
                        elif score >= 7.0:
                            item.verdict = 'WW'
                        elif score >= 5.0:
                            item.verdict = 'OTW'
                        else:
                            item.verdict = 'SKIP'
                        
                        if score > 7.5 and not item.is_featured:
                            import random
                            if random.random() < 0.2:
                                item.is_hidden_gem = True
                                
                        item.save()
                        self.stdout.write(f"  Synced: {item.title}")

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully synced {pages} pages of content!'))
