import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialAuthProject.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def cleanup_and_setup():
    # Setup Site
    site, created = Site.objects.get_or_create(id=1, defaults={'domain': '127.0.0.1:8000', 'name': '127.0.0.1:8000'})
    
    # Providers we care about
    providers = ['google', 'facebook', 'github']
    
    for provider in providers:
        # Get all apps for this provider
        apps = SocialApp.objects.filter(provider=provider)
        
        if apps.count() > 1:
            print(f"Found {apps.count()} apps for {provider}. Cleaning up...")
            # Keep the first one, delete the rest
            first_app = apps.first()
            apps.exclude(id=first_app.id).delete()
            app = first_app
        elif apps.count() == 1:
            app = apps.first()
        else:
            print(f"Creating new SocialApp for {provider}")
            app = SocialApp.objects.create(
                provider=provider,
                name=provider.capitalize(),
                client_id='placeholder-id',
                secret='placeholder-secret'
            )
        
        # Ensure it's linked to the correct site
        app.sites.add(site)
        print(f"Ensured unique SocialApp for {provider} linked to site {site.domain}")

if __name__ == "__main__":
    cleanup_and_setup()
