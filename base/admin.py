from django.contrib import admin
from .models import User, Mentor, Chat, ChatRoom
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.site_header = 'MentorMentee Admin'
admin.site.register(User, UserAdmin)

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'job_title', 'price', 'category', 'skill']
    search_fields = ['name', 'email', 'job_title', 'price', 'category', 'skill', 'description']

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['message', 'sender', 'reciever', 'room']
    search_fields = ['message', 'sender', 'reciever', 'room']
