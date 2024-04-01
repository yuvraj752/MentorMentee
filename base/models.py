from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    TYPES = {
        'mentor': 'Mentor',
        'mentee': 'Mentee',
    }
    type = models.CharField(max_length=25, choices=TYPES, default='mentee')

    def unread_chat_count(self):
        return self.recieved_chats.filter(is_read=False).count()

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
    
    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return self.name.title()
    
class ChatRoom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.name
    
    def last_chat(self):
        return self.chat_set.last()
    
    def unread_chat_count(self):
        return self.chat_set.filter(is_read=False).count()

class Chat(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='sent_chats'
    )
    reciever = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='recieved_chats'
    )
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE) 
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.message
