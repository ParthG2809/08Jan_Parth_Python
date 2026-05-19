import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialAuthProject.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def sync_env_to_db():
    # Update Site to current host (assuming 127.0.0.1:8000)
    site = Site.objects.get(id=1)
    site.domain = '127.0.0.1:8000'
    site.name = '127.0.0.1:8000'
    site.save()
    print(f"Site updated to {site.domain}")

    # Map providers to env vars
    mapping = {
        'google': ('GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET'),
        'github': ('GITHUB_CLIENT_ID', 'GITHUB_CLIENT_SECRET'),
        'facebook': ('FACEBOOK_CLIENT_ID', 'FACEBOOK_CLIENT_SECRET'),
    }

    for provider, (id_var, secret_var) in mapping.items():
        client_id = os.getenv(id_var)
        secret = os.getenv(secret_var)

        if client_id and client_id != 'placeholder-id':
            app = SocialApp.objects.get(provider=provider)
            app.client_id = client_id
            app.secret = secret
            app.save()
            print(f"Successfully synced {provider} credentials from .env")
        else:
            print(f"Skipping {provider}: No valid credentials found in .env (still placeholder)")

if __name__ == "__main__":
    sync_env_to_db()
