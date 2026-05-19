import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialAuthProject.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def nuclear_cleanup():
    print("Starting nuclear cleanup of SocialApps and Sites...")
    
    # Delete all SocialApps
    SocialApp.objects.all().delete()
    print("Deleted all SocialApps.")
    
    # Delete all Sites except maybe one if we want to be safe, but let's just clear it
    Site.objects.all().delete()
    print("Deleted all Sites.")
    
    # Recreate the main Site
    site = Site.objects.create(id=1, domain='127.0.0.1:8000', name='127.0.0.1:8000')
    print(f"Recreated Site: {site.domain} (ID: {site.id})")
    
    # Recreate the SocialApps
    providers = ['google', 'facebook', 'github']
    for provider in providers:
        app = SocialApp.objects.create(
            provider=provider,
            name=provider.capitalize(),
            client_id='placeholder-id',
            secret='placeholder-secret'
        )
        app.sites.add(site)
        print(f"Created clean SocialApp for {provider}.")

if __name__ == "__main__":
    nuclear_cleanup()
