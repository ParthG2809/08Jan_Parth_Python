from django.urls import reverse
from django.db import transaction
from django.db.models.signals import post_save
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from .models import Doctor

class DoctorAPITests(APITestCase):
    """
    Comprehensive test suite for the Doctor REST API.
    Covers CRUD, Pagination, Ordering, Validation, and Transaction Rollback safety.
    """

    def setUp(self):
        # Create some initial test doctor data
        self.doc1 = Doctor.objects.create(
            name="Alice Smith",
            specialization="Cardiologist",
            experience_years=10,
            email="alice.smith@example.com",
            phone_number="+15550000001",
            clinic_address="123 Heart St, Boston, MA",
            consultation_fee=Decimal("150.00"),
            is_active=True
        )
        self.doc2 = Doctor.objects.create(
            name="Bob Jones",
            specialization="Pediatrician",
            experience_years=5,
            email="bob.jones@example.com",
            phone_number="+15550000002",
            clinic_address="456 Kid Ave, New York, NY",
            consultation_fee=Decimal("100.00"),
            is_active=True
        )
        self.list_create_url = reverse('doctor-list')
        self.detail_url = lambda pk: reverse('doctor-detail', kwargs={'pk': pk})

    # ==========================================
    # 1. CRUD & VALIDATION TESTS
    # ==========================================

    def test_create_doctor_success(self):
        """Verify successful doctor profile creation."""
        data = {
            "name": "Charlie Brown",
            "specialization": "Dermatologist",
            "experience_years": 8,
            "email": "charlie.b@example.com",
            "phone_number": "+15550000003",
            "clinic_address": "789 Skin Blvd, Miami, FL",
            "consultation_fee": "120.00",
            "is_active": True
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Doctor.objects.count(), 3)
        self.assertEqual(Doctor.objects.get(email="charlie.b@example.com").name, "Charlie Brown")

    def test_create_doctor_negative_fee_fail(self):
        """Verify that negative consultation fee validation fails."""
        data = {
            "name": "Charlie Brown",
            "specialization": "Dermatologist",
            "experience_years": 8,
            "email": "charlie.b@example.com",
            "phone_number": "+15550000003",
            "clinic_address": "789 Skin Blvd, Miami, FL",
            "consultation_fee": "-10.00",
            "is_active": True
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("consultation_fee", response.data)

    def test_create_active_doctor_without_contact_fail(self):
        """Verify that active doctor profile requires at least phone_number or clinic_address."""
        data = {
            "name": "Charlie Brown",
            "specialization": "Dermatologist",
            "experience_years": 8,
            "email": "charlie.b@example.com",
            "consultation_fee": "120.00",
            "is_active": True  # Active, but phone and clinic_address are omitted
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Should raise non_field_errors validation error
        self.assertIn("non_field_errors", response.data)
        self.assertIn("at least one contact method", response.data["non_field_errors"][0])

    def test_retrieve_doctor_detail(self):
        """Verify retrieving details of a single doctor profile."""
        response = self.client.get(self.detail_url(self.doc1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Alice Smith")
        self.assertEqual(response.data["specialization"], "Cardiologist")

    def test_update_doctor_success(self):
        """Verify successfully updating a doctor profile."""
        data = {
            "name": "Alice Smith",
            "specialization": "Cardiologist",
            "experience_years": 11,  # increment years
            "email": "alice.smith@example.com",
            "phone_number": "+15550000001",
            "clinic_address": "123 Heart St, Boston, MA",
            "consultation_fee": "160.00",  # raise fee
            "is_active": True
        }
        response = self.client.put(self.detail_url(self.doc1.pk), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.doc1.refresh_from_db()
        self.assertEqual(self.doc1.experience_years, 11)
        self.assertEqual(self.doc1.consultation_fee, Decimal("160.00"))

    def test_delete_doctor_success(self):
        """Verify successfully deleting a doctor profile."""
        response = self.client.delete(self.detail_url(self.doc1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Doctor.objects.count(), 1)

    # ==========================================
    # 2. PAGINATION, ORDERING & SEARCH TESTS
    # ==========================================

    def test_limit_offset_pagination(self):
        """Verify standard LimitOffsetPagination behavior."""
        # Query with limit=1
        response = self.client.get(self.list_create_url, {'limit': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["count"], 2)
        self.assertIsNotNone(response.data["next"])

    def test_ordering_by_name_ascending(self):
        """Verify client-side ordering by name (ascending)."""
        response = self.client.get(self.list_create_url, {'ordering': 'name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        # Alice Smith should come before Bob Jones
        self.assertEqual(results[0]["name"], "Alice Smith")
        self.assertEqual(results[1]["name"], "Bob Jones")

    def test_ordering_by_fee_descending(self):
        """Verify client-side ordering by consultation_fee (descending)."""
        response = self.client.get(self.list_create_url, {'ordering': '-consultation_fee'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        # doc1 (150.00) should come before doc2 (100.00)
        self.assertEqual(Decimal(results[0]["consultation_fee"]), Decimal("150.00"))
        self.assertEqual(Decimal(results[1]["consultation_fee"]), Decimal("100.00"))

    def test_search_specialization(self):
        """Verify filtering doctor list using query searches."""
        response = self.client.get(self.list_create_url, {'search': 'Cardiologist'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # LimitOffsetPagination results field
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Alice Smith")

    # ==========================================
    # 3. ATOMIC TRANSACTION ROLLBACK TESTS
    # ==========================================

    def test_transaction_rollback_on_failed_save(self):
        """
        Verify that database modifications roll back completely in case of mid-save failure,
        guaranteeing atomic integrity.
        """
        # Define a post-save signal listener that deliberately crashes
        def error_trigger(sender, instance, **kwargs):
            raise RuntimeError("Simulated unexpected database write crash")

        # Register the post-save signal listener on Doctor
        post_save.connect(error_trigger, sender=Doctor)

        new_doctor_data = {
            "name": "Dr. Disaster",
            "specialization": "General Practitioner",
            "experience_years": 3,
            "email": "dr.disaster@example.com",
            "phone_number": "+15559999999",
            "clinic_address": "999 Danger Zone, Nowhere",
            "consultation_fee": "50.00",
            "is_active": True
        }

        try:
            # Send API request. The view wraps this in transaction.atomic.
            # During creation, it will write to DB and then trigger post_save.
            # Post-save will raise a RuntimeError, which will bubble up.
            response = self.client.post(self.list_create_url, new_doctor_data, format='json')
        except RuntimeError:
            pass  # Expecting the runtime crash to occur and bubble up
        finally:
            # MUST unregister the crash listener so other tests are not impacted
            post_save.disconnect(error_trigger, sender=Doctor)

        # ASSERTION: The doctor profile must NOT exist in the database!
        # Without transaction.atomic, the database insert statement would have already
        # successfully committed before post_save executed, persisting Dr. Disaster.
        # With transaction.atomic, the error triggers a database rollback.
        doctor_exists = Doctor.objects.filter(email="dr.disaster@example.com").exists()
        self.assertFalse(doctor_exists, "Database transaction failed to roll back! 'Dr. Disaster' was incorrectly saved.")
