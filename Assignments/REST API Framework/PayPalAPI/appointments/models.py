from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=100)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialty}"

class Appointment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
    ]

    patient_name = models.CharField(max_length=200)
    patient_email = models.EmailField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    paypal_order_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Appointment: {self.patient_name} with {self.doctor.name} on {self.date}"
