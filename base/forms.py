from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms

class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'type']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): 
            field.help_text = None
