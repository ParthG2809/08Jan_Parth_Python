from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from decimal import Decimal

class Doctor(models.Model):
    name = models.CharField(max_length=100, help_text="Full name of the doctor.")
    specialization = models.CharField(max_length=100, help_text="Specialization of the doctor (e.g., Cardiologist).")
    experience_years = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Years of clinical experience."
    )
    email = models.EmailField(unique=True, help_text="Email address of the doctor (must be unique).")
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        help_text="Contact phone number."
    )
    clinic_address = models.TextField(blank=True, null=True, help_text="Physical address of the clinic.")
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Consultation fee per visit."
    )
    is_active = models.BooleanField(default=True, help_text="Designates whether this doctor profile is active.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"
