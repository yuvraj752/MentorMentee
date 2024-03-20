from django.forms import ModelForm
from .models import Mentor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField

class MentorForm(ModelForm):
    class Meta:
        model = Mentor
        fields = ['name', 'email', 'job_title', 'price', 
                  'category', 'skill', 'image', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        field_divs = []
        for field_name in self.fields.keys():
            if field_name in ['image', 'description']:
                 field_divs.append(Div(field_name, css_class='col-md-12')) 
            else:
                field_divs.append(Div(FloatingField(field_name), css_class='col-md-6')) 
        self.helper.layout = Layout(Div(*field_divs, css_class='row'), 
            Submit('submit', 'Submit', css_class='btn btn-primary w-100'))