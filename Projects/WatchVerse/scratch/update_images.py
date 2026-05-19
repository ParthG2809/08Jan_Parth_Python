import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WatchVerse.settings')
django.setup()

from accounts.models import MediaItem

def update_images():
    dune = MediaItem.objects.filter(title='Dune: Part Two').first()
    if dune:
        dune.backdrop = 'backdrops/dune_backdrop.png'
        dune.poster = 'posters/dune_backdrop.png' # Using same for poster dummy
        dune.save()
        print("Updated Dune")

    cyberpunk = MediaItem.objects.filter(title='Cyberpunk: Edgerunners').first()
    if cyberpunk:
        cyberpunk.poster = 'posters/edgerunners_poster.png'
        cyberpunk.backdrop = 'posters/edgerunners_poster.png'
        cyberpunk.save()
        print("Updated Cyberpunk")

if __name__ == '__main__':
    update_images()
