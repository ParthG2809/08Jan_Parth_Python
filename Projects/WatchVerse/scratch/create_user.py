import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WatchVerse.settings')
django.setup()

from accounts.models import User

def create_test_user():
    email = 'test@example.com'
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(email=email, password='password123', full_name='Test User')
        user.is_verified = True
        user.save()
        print(f"Created user {email}")
    else:
        print(f"User {email} already exists")

if __name__ == '__main__':
    create_test_user()
