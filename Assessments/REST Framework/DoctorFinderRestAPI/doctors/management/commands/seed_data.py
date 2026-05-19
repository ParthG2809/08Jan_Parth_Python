from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from doctors.models import Doctor

class Command(BaseCommand):
    help = 'Seeds the database with 15 highly realistic doctor profiles.'

    def handle(self, *args, **options):
        doctors_data = [
            {
                "name": "Sarah Connor",
                "specialization": "Cardiologist",
                "experience_years": 14,
                "email": "sarah.connor@cardiohealth.com",
                "phone_number": "+15550192834",
                "clinic_address": "Cardiology Center, Suite 400, Los Angeles, CA",
                "consultation_fee": Decimal("150.00"),
                "is_active": True
            },
            {
                "name": "Gregory House",
                "specialization": "Diagnostic Medicine",
                "experience_years": 25,
                "email": "g.house@princetonplainsboro.org",
                "phone_number": "+15559876543",
                "clinic_address": "Department of Diagnostics, Princeton Plainsboro Teaching Hospital, NJ",
                "consultation_fee": Decimal("350.00"),
                "is_active": True
            },
            {
                "name": "Stephen Strange",
                "specialization": "Neurosurgeon",
                "experience_years": 16,
                "email": "s.strange@metrogeneral.org",
                "phone_number": "+15554321098",
                "clinic_address": "Metro General Hospital, Neuro Wing, New York, NY",
                "consultation_fee": Decimal("500.00"),
                "is_active": True
            },
            {
                "name": "John Watson",
                "specialization": "General Practitioner",
                "experience_years": 12,
                "email": "j.watson@bakerstreetclinic.co.uk",
                "phone_number": "+442079460192",
                "clinic_address": "221B Baker Street Surgery, London",
                "consultation_fee": Decimal("75.00"),
                "is_active": True
            },
            {
                "name": "Leonard McCoy",
                "specialization": "Space Medicine",
                "experience_years": 20,
                "email": "bones@starfleet.med",
                "phone_number": "+15557778888",
                "clinic_address": "Starfleet Headquarters Medical Bay, San Francisco, CA",
                "consultation_fee": Decimal("200.00"),
                "is_active": True
            },
            {
                "name": "Meredith Grey",
                "specialization": "General Surgeon",
                "experience_years": 15,
                "email": "m.grey@grey-sloan.org",
                "phone_number": "+15555550101",
                "clinic_address": "Grey Sloan Memorial Hospital, Seattle, WA",
                "consultation_fee": Decimal("180.00"),
                "is_active": True
            },
            {
                "name": "Dana Scully",
                "specialization": "Forensic Pathologist",
                "experience_years": 18,
                "email": "d.scully@fbi.gov",
                "phone_number": "+15550112233",
                "clinic_address": "FBI HQ Medical Lab, Washington, D.C.",
                "consultation_fee": Decimal("120.00"),
                "is_active": True
            },
            {
                "name": "Hannibal Lecter",
                "specialization": "Psychiatrist",
                "experience_years": 22,
                "email": "h.lecter@baltimoreoffice.com",
                "phone_number": "+15556667777",
                "clinic_address": "8 East Chase Street, Baltimore, MD",
                "consultation_fee": Decimal("400.00"),
                "is_active": False
            },
            {
                "name": "Shaun Murphy",
                "specialization": "Pediatric Surgeon",
                "experience_years": 8,
                "email": "s.murphy@sanjosebonaventure.org",
                "phone_number": "+15552345678",
                "clinic_address": "San Jose St. Bonaventure Hospital, Pediatric Wing, CA",
                "consultation_fee": Decimal("130.00"),
                "is_active": True
            },
            {
                "name": "Fiona Gallagher",
                "specialization": "Dermatologist",
                "experience_years": 9,
                "email": "fiona.g@dermcare.com",
                "phone_number": "+15558901234",
                "clinic_address": "DermCare Center, Chicago, IL",
                "consultation_fee": Decimal("90.00"),
                "is_active": True
            },
            {
                "name": "Rajesh Koothrappali",
                "specialization": "Pediatrician",
                "experience_years": 10,
                "email": "raj.k@pasadenapediatrics.com",
                "phone_number": "+15557894561",
                "clinic_address": "Pasadena Pediatrics, Suite 101, Pasadena, CA",
                "consultation_fee": Decimal("110.00"),
                "is_active": True
            },
            {
                "name": "Amy Farrah Fowler",
                "specialization": "Neurobiologist",
                "experience_years": 11,
                "email": "amy.ff@braininstitute.edu",
                "phone_number": "+15556543210",
                "clinic_address": "Institute of Brain Science, Pasadena, CA",
                "consultation_fee": Decimal("160.00"),
                "is_active": True
            },
            {
                "name": "Jack Shephard",
                "specialization": "Spinal Surgeon",
                "experience_years": 13,
                "email": "j.shephard@spinalcenter.com",
                "phone_number": "+15559871234",
                "clinic_address": "St. Sebastian Medical Center, Los Angeles, CA",
                "consultation_fee": Decimal("250.00"),
                "is_active": True
            },
            {
                "name": "Doogie Howser",
                "specialization": "Pediatric Resident",
                "experience_years": 5,
                "email": "doogie.h@eastmanmedical.org",
                "phone_number": "+15553216540",
                "clinic_address": "Eastman Medical Center, Los Angeles, CA",
                "consultation_fee": Decimal("85.00"),
                "is_active": True
            },
            {
                "name": "Christian Troy",
                "specialization": "Plastic Surgeon",
                "experience_years": 17,
                "email": "c.troy@mcnamaratroy.com",
                "phone_number": "+15558889999",
                "clinic_address": "McNamara/Troy Plastic Surgery, Miami, FL",
                "consultation_fee": Decimal("450.00"),
                "is_active": True
            }
        ]

        self.stdout.write("Seeding doctor profiles...")
        created_count = 0
        skipped_count = 0

        with transaction.atomic():
            for doc in doctors_data:
                if Doctor.objects.filter(email=doc["email"]).exists():
                    skipped_count += 1
                else:
                    Doctor.objects.create(**doc)
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded! Created {created_count} profiles, skipped {skipped_count} existing profiles."
            )
        )
