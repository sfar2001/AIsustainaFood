from django.contrib.auth.models import AbstractUser
from django.db import models  # Add this import


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username



