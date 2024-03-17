from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    TYPES = {
        'mentor': 'Mentor',
        'mentee': 'Mentee',
    }
    type = models.CharField(max_length=25, choices=TYPES, default='mentee')
