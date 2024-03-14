from django.db import models
from base.models import User

# Create your models here.
class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField()
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