from django.db import models

# Create your models here.
class shivu(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    address=models.TextField()
