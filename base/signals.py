from .models import User
from .models import Mentor
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify

@receiver(post_save, sender=User)
def create_mentor_profile(sender, instance, created, **kwargs):
    user = instance
    if created and user.type == 'mentor':
        slug = slugify(user.first_name)
        num = 1
        while Mentor.objects.filter(slug=slug).exists():
            slug = f"{slug}-{num}"
            num += 1
        Mentor.objects.create(user=user, name=user.first_name, 
                              slug=slug, email=user.email)

@receiver(post_delete, sender=Mentor)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
