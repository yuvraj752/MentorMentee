from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    TYPES = {
        'mentor': 'Mentor',
        'mentee': 'Mentee',
    }
    type = models.CharField(max_length=25, choices=TYPES, default='mentee')

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='images')
    email = models.EmailField(max_length=254)
    job_title = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=50, blank=True)
    skill = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name.title()
    
    class Meta:
        ordering = ['created']

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.CharField(max_length=50)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ['created']
 