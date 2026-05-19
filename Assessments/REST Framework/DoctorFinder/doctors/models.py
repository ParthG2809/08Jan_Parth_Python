from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name} - {self.specialization} ({self.city})"
