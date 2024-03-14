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
        self.fields['type'].choices = [('', 'Select an option')] + list(self.fields['type'].choices)[1:]
        self.fields["type"].widget.attrs.update({"class": "form-select my-2", "id": "floatType", 'placeholder':'type'})
        
        self.fields["username"].widget.attrs.update({'class': 'form-control my-2', "id": "floatUsername", 'placeholder':'username'})
        self.fields["first_name"].widget.attrs.update({'class': 'form-control my-2', "id": "floatFirstName", 'placeholder':'first_name'})
        self.fields["email"].widget.attrs.update({'class': 'form-control my-2', "id": "floatEmail", 'placeholder':'email'})
        self.fields["password1"].widget.attrs.update({'class': 'form-control my-2', "id": "floatPassword1", 'placeholder':'password1'})
        self.fields["password2"].widget.attrs.update({'class': 'form-control my-2', "id": "floatInputPassword2", 'placeholder':'password2'})
        
        for field in self.fields.values():
            field.help_text = None

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"id": "floatUsername", 'placeholder':'username'})
        self.fields["password"].widget.attrs.update({"id": "floatPassword", 'placeholder':'password'})
        for field in self.fields.values(): 
            field.widget.attrs.update({'class': 'form-control my-2'})
