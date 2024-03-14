from .models import User
from mentors.models import Mentor
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_mentor_profile(sender, instance, created, **kwargs):
    user = instance
    if created and user.type == 'mentor':
        Mentor.objects.create(user=user, name=user.first_name, 
                              slug=user.username, email=user.email)

@receiver(post_delete, sender=Mentor)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
