import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DoctorsGoogleMaps.settings")
django.setup()

from doctors.models import Doctor

def seed_data():
    doctors_data = [
        {
            'name': 'Dr. Alice Smith',
            'specialty': 'Cardiologist',
            'address': '123 Heart Center',
            'city': 'New York',
            'latitude': 40.7128,
            'longitude': -74.0060,
        },
        {
            'name': 'Dr. Bob Johnson',
            'specialty': 'Dermatologist',
            'address': '456 Skin Clinic',
            'city': 'New York',
            'latitude': 40.7580,
            'longitude': -73.9855,
        },
        {
            'name': 'Dr. Charlie Brown',
            'specialty': 'Pediatrician',
            'address': '789 Child Care',
            'city': 'Los Angeles',
            'latitude': 34.0522,
            'longitude': -118.2437,
        },
        {
            'name': 'Dr. Diana Prince',
            'specialty': 'Orthopedic',
            'address': '321 Bone Health',
            'city': 'Chicago',
            'latitude': 41.8781,
            'longitude': -87.6298,
        },
        {
            'name': 'Dr. Evan Wright',
            'specialty': 'Neurologist',
            'address': '654 Brain Institute',
            'city': 'New York',
            'latitude': 40.7829,
            'longitude': -73.9654,
        }
    ]

    for data in doctors_data:
        Doctor.objects.get_or_create(**data)
        print(f"Added {data['name']}")

if __name__ == '__main__':
    seed_data()
