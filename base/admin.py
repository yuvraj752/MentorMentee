from django.contrib import admin
from .models import User, Mentor, Chat
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Mentor)
admin.site.register(Chat)
