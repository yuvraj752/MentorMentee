from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    TYPES = {
        'mentor': 'Mentor',
        'mentee': 'Mentee',
    }
    type = models.CharField(max_length=25, choices=TYPES)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recieved_messages')
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('is_read', '-created',)
    
    def __str__(self):
        return f'{self.sender.get_full_name().title()} to {self.reciever.get_full_name().title()}'
