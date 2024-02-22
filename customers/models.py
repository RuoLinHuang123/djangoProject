from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields like rating, author, etc. as needed

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
