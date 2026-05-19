import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialAuthProject.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_social_apps():
    # Setup Site
    site, created = Site.objects.get_or_create(id=1, defaults={'domain': '127.0.0.1:8000', 'name': '127.0.0.1:8000'})
    if not created:
        site.domain = '127.0.0.1:8000'
        site.name = '127.0.0.1:8000'
        site.save()

    # Setup Providers
    providers = ['google', 'facebook', 'github']
    for provider in providers:
        app, created = SocialApp.objects.get_or_create(
            provider=provider,
            defaults={
                'name': provider.capitalize(),
                'client_id': 'placeholder-id',
                'secret': 'placeholder-secret',
            }
        )
        app.sites.add(site)
        print(f"Ensured SocialApp for {provider} exists.")

if __name__ == "__main__":
    setup_social_apps()
