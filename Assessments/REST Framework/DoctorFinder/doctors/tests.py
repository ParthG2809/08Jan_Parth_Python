from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Doctor

class DoctorAPITests(APITestCase):
    def setUp(self):
        # Create 12 test doctors to test pagination with page size = 5
        for i in range(12):
            Doctor.objects.create(
                name=f"Dr. Doctor {i}",
                specialization="General Medicine",
                city="San Francisco"
            )

    def test_create_doctor(self):
        url = reverse('doctor-list')
        data = {
            "name": "Dr. Gregory House",
            "specialization": "Diagnostic Medicine",
            "city": "Princeton"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Dr. Gregory House")
        self.assertEqual(response.data['specialization'], "Diagnostic Medicine")
        self.assertEqual(response.data['city'], "Princeton")

    def test_paginated_doctor_list(self):
        url = reverse('doctor-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check pagination is working: 5 items per page (as settings.py PAGE_SIZE = 5)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['count'], 12)
