from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import PasswordChangeForm
from .models import Donor

class DonorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class DonorForm(forms.ModelForm):
    class Meta:
        model=models.Donor
        fields=['bloodgroup','address','mobile','profile_pic']

class DonationForm(forms.ModelForm):
    class Meta:
        model=models.BloodDonate
        fields=['age','bloodgroup','disease','unit']

class UpdateUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class UpdatePasswordForm(PasswordChangeForm):
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
        
class DonorEligibilityForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['age', 'weight', 'has_health_issues', 'last_donation_date']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your weight in kg'}),
            'has_health_issues': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'last_donation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }