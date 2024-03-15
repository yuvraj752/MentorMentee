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
        for field_name, field in self.fields.items():
            if field_name == 'type':
                field.choices = [('', 'Select an option')] + list(field.choices)[1:]
                field.widget.attrs.update({"class": "form-select"})
                if field_name in self.errors:
                    field.widget.attrs.update({'class': 'form-select is-invalid'})
            else: 
                field.widget.attrs.update({'class': 'form-control'})
                if field_name in self.errors:
                    field.widget.attrs.update({'class': 'form-control is-invalid'})
            field.widget.attrs.update({'placeholder':'placeholder'})
            field.help_text = None

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder':'placeholder'})
            if self.errors:
                field.widget.attrs.update({'class': 'form-control is-invalid'})
