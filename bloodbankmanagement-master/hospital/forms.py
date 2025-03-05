from django import forms
from django.contrib.auth.models import User
from . import models

# Hospital User Form (for registration)
class HospitalUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

# Hospital Profile Form (for registration)
class HospitalForm(forms.ModelForm):
    class Meta:
        model = models.Hospital
        fields = ['name', 'address', 'contact_number', 'email']