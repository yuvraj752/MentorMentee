from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, AuthenticationForm
from .models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField

class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='Full Name')
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'type']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        field_divs = []
        for field_name, field in self.fields.items(): 
            field.help_text = None
            field_divs.append(Div(FloatingField(field_name), css_class='col-md-6')) 
        self.helper.layout = Layout(Div(*field_divs, css_class='row'), 
                                    Submit('submit', 'Register', css_class='btn btn-primary w-100'))

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        field_divs = []
        for field_name, field in self.fields.items(): 
            field_divs.append(Div(FloatingField(field_name), css_class='col-md-12')) 
        self.helper.layout = Layout(Div(*field_divs, css_class='row'), 
                                    Submit('submit', 'Login', css_class='btn btn-primary w-100 mb-2'))


class SetPasswordForm(SetPasswordForm):
    class Meta:
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): field.help_text = None
